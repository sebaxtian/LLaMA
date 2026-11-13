#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/git/verify_branch_protection.py

Auditor y validador determinista de la configuración remota de GitHub.
Comprueba que los ajustes del repositorio (métodos de fusión) y las reglas
de protección de ramas (main y dev) convergen estrictamente con las
especificaciones declarativas en tools/git/protection_rules/.

Códigos de salida:
  0: Configuración remota plenamente convergida con la especificación.
  1: Desvíos detectados en ajustes de repositorio o protección de ramas.
  2: Error de autenticación, conectividad o invocación.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def get_git_credential_token() -> str | None:
    """Intenta obtener el token de autenticación de GitHub desde Git Credential Manager."""
    try:
        res = subprocess.run(
            ["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\n\n",
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        if res.returncode == 0 and res.stdout:
            creds = dict(
                line.split("=", 1)
                for line in res.stdout.strip().splitlines()
                if "=" in line
            )
            val = creds.get("password")
            if val and val.strip():
                return val.strip()
    except (FileNotFoundError, PermissionError, subprocess.SubprocessError):
        pass
    return None


def get_github_token(cli_token: str | None = None) -> str | None:
    """Obtiene el token de autenticación de GitHub siguiendo la precedencia:
    1. Parámetro CLI explícito (--token).
    2. Variable de entorno GITHUB_PERSONAL_ACCESS_TOKEN.
    3. Variable de entorno GITHUB_TOKEN.
    4. Variable de entorno GH_TOKEN.
    5. Comando `gh auth token` (GitHub CLI) si está disponible en PATH.
    6. Git Credential Manager (`git credential fill`).
    """
    if cli_token and cli_token.strip():
        return cli_token.strip()

    for env_var in ("GITHUB_PERSONAL_ACCESS_TOKEN", "GITHUB_TOKEN", "GH_TOKEN"):
        val = os.environ.get(env_var)
        if val and val.strip():
            return val.strip()

    try:
        res = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except (FileNotFoundError, PermissionError, subprocess.SubprocessError):
        pass

    return get_git_credential_token()


def get_repo_owner_and_name() -> tuple[str | None, str | None]:
    """Detecta el propietario y nombre del repositorio desde el remoto git 'origin'."""
    try:
        res = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        if res.returncode == 0:
            url = res.stdout.strip()
            if url.endswith(".git"):
                url = url[:-4]
            if "github.com/" in url:
                parts = url.split("github.com/")[1].split("/")
                if len(parts) >= 2:
                    return parts[0], parts[1]
            elif "github.com:" in url:
                parts = url.split("github.com:")[1].split("/")
                if len(parts) >= 2:
                    return parts[0], parts[1]
    except (FileNotFoundError, PermissionError, subprocess.SubprocessError):
        pass

    return None, None


def github_api_request(
    url: str,
    method: str = "GET",
    data: dict[str, Any] | None = None,
    token: str | None = None,
) -> tuple[int, Any, str | None]:
    """Ejecuta una petición a la API REST v3 de GitHub utilizando urllib."""
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "LLaMA-Branch-Protection-Verifier",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    body_bytes = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body_bytes, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            raw_body = resp.read().decode("utf-8")
            parsed = json.loads(raw_body) if raw_body else None
            return status, parsed, None
    except urllib.error.HTTPError as err:
        err_body = err.read().decode("utf-8", errors="replace")
        try:
            err_json = json.loads(err_body)
            msg = err_json.get("message", err_body)
            errors = err_json.get("errors")
            if errors:
                err_msg = f"{msg}: {errors}"
            else:
                err_msg = msg
        except Exception:
            err_json = None
            err_msg = err_body
        return err.code, err_json, err_msg
    except urllib.error.URLError as err:
        return 0, None, f"Error de red o conexión: {err.reason}"
    except Exception as err:
        return 0, None, f"Excepción imprevista: {err}"


def compare_repo_settings_dicts(actual: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    """Compara los ajustes reales del repositorio con la especificación canónica esperada."""
    discrepancies: list[str] = []

    # Métodos de fusión mandatorios por gobernanza constitucional
    core_keys = ["allow_merge_commit", "allow_squash_merge", "allow_rebase_merge"]
    for k in core_keys:
        if k in expected:
            expected_val = expected[k]
            actual_val = actual.get(k)
            if actual_val != expected_val:
                discrepancies.append(
                    f"Ajuste '{k}': esperado={expected_val}, actual={actual_val}"
                )

    # Ajustes opcionales presentes en la especificación JSON
    extra_keys = ["delete_branch_on_merge", "allow_auto_merge"]
    for k in extra_keys:
        if k in expected:
            expected_val = expected[k]
            actual_val = actual.get(k)
            if actual_val != expected_val:
                discrepancies.append(
                    f"Ajuste '{k}': esperado={expected_val}, actual={actual_val}"
                )

    return discrepancies


def _extract_enabled(val: Any) -> Any:
    """Extrae el valor booleano o representativo de objetos {'enabled': bool} de GitHub API."""
    if isinstance(val, dict) and "enabled" in val:
        return val["enabled"]
    return val


def compare_protection_dicts(
    actual: dict[str, Any],
    expected: dict[str, Any],
    is_user_repo: bool = False,
) -> list[str]:
    """Compara las reglas de protección reales devueltas por GitHub con la especificación canónica."""
    discrepancies: list[str] = []

    # 1. enforce_admins
    if "enforce_admins" in expected:
        exp_admins = expected["enforce_admins"]
        act_admins = _extract_enabled(actual.get("enforce_admins"))
        if act_admins != exp_admins:
            discrepancies.append(
                f"enforce_admins: esperado={exp_admins}, actual={act_admins}"
            )

    # 2. required_pull_request_reviews
    exp_reviews = expected.get("required_pull_request_reviews")
    act_reviews = actual.get("required_pull_request_reviews")
    if exp_reviews is not None:
        if act_reviews is None:
            discrepancies.append(
                "required_pull_request_reviews: esperado configurado, pero no está habilitado (null)"
            )
        elif isinstance(act_reviews, dict):
            for subkey in (
                "required_approving_review_count",
                "dismiss_stale_reviews",
                "require_code_owner_reviews",
                "require_last_push_approval",
            ):
                if subkey in exp_reviews:
                    exp_val = exp_reviews[subkey]
                    act_val = act_reviews.get(subkey)
                    if act_val != exp_val:
                        discrepancies.append(
                            f"required_pull_request_reviews.{subkey}: esperado={exp_val}, actual={act_val}"
                        )
    elif act_reviews is not None:
        discrepancies.append(
            f"required_pull_request_reviews: esperado=None, actual={act_reviews}"
        )

    # 3. restrictions (bloqueo de push directo fuera de PR)
    exp_restrictions = expected.get("restrictions")
    act_restrictions = actual.get("restrictions")
    if exp_restrictions is not None:
        if act_restrictions is None:
            # En repositorios personales (User), GitHub API no admite el objeto restrictions
            # (devuelve HTTP 422 'Only organization repositories can have users and team restrictions').
            # En dicho entorno, el bloqueo de push directo se garantiza mediante required_pull_request_reviews
            # y enforce_admins: true. Solo se reporta discrepancia si no es repositorio personal.
            if not is_user_repo:
                discrepancies.append(
                    "restrictions: esperado configurado (bloqueo de push directo), pero está desactivado (null)"
                )
        elif isinstance(act_restrictions, dict):
            # Extraer nombres o slugs de usuarios, equipos y aplicaciones
            actual_users = [
                u.get("login", u) if isinstance(u, dict) else u
                for u in act_restrictions.get("users", [])
            ]
            expected_users = exp_restrictions.get("users", [])
            if sorted(str(x) for x in actual_users) != sorted(str(x) for x in expected_users):
                discrepancies.append(
                    f"restrictions.users: esperado={expected_users}, actual={actual_users}"
                )

            actual_teams = [
                t.get("slug", t) if isinstance(t, dict) else t
                for t in act_restrictions.get("teams", [])
            ]
            expected_teams = exp_restrictions.get("teams", [])
            if sorted(str(x) for x in actual_teams) != sorted(str(x) for x in expected_teams):
                discrepancies.append(
                    f"restrictions.teams: esperado={expected_teams}, actual={actual_teams}"
                )

            actual_apps = [
                a.get("slug", a) if isinstance(a, dict) else a
                for a in act_restrictions.get("apps", [])
            ]
            expected_apps = exp_restrictions.get("apps", [])
            if sorted(str(x) for x in actual_apps) != sorted(str(x) for x in expected_apps):
                discrepancies.append(
                    f"restrictions.apps: esperado={expected_apps}, actual={actual_apps}"
                )
    elif act_restrictions is not None:
        discrepancies.append(f"restrictions: esperado=None, actual={act_restrictions}")

    # 4. Parámetros booleanos simples
    bool_keys = [
        "allow_force_pushes",
        "allow_deletions",
        "block_creations",
        "required_conversation_resolution",
        "required_linear_history",
        "lock_branch",
        "allow_fork_syncing",
    ]
    for k in bool_keys:
        if k in expected:
            exp_val = expected[k]
            act_val = _extract_enabled(actual.get(k))
            if act_val != exp_val:
                discrepancies.append(f"{k}: esperado={exp_val}, actual={act_val}")

    # 5. required_status_checks
    exp_status = expected.get("required_status_checks")
    act_status = actual.get("required_status_checks")
    if exp_status is None:
        if act_status is not None:
            # Si contiene contextos o checks activos
            checks = act_status.get("checks", [])
            contexts = act_status.get("contexts", [])
            if checks or contexts:
                discrepancies.append(
                    f"required_status_checks: esperado=None, actual checks={checks or contexts}"
                )
    elif isinstance(exp_status, dict):
        if act_status is None:
            discrepancies.append("required_status_checks: esperado configurado, actual=None")

    return discrepancies


def verify_repo_settings(
    owner: str,
    repo: str,
    expected_config: dict[str, Any] | None = None,
    token: str | None = None,
    api_base_url: str = "https://api.github.com",
) -> list[str]:
    """Evalúa que allow_merge_commit == True, allow_squash_merge == False y allow_rebase_merge == False
    conforme a la firma y contrato de SPEC-007 plan.md.
    """
    if expected_config is None:
        expected_config = {
            "allow_merge_commit": True,
            "allow_squash_merge": False,
            "allow_rebase_merge": False,
        }

    tok = get_github_token(token)
    url = f"{api_base_url.rstrip('/')}/repos/{owner}/{repo}"
    status, data, err_msg = github_api_request(url, method="GET", token=tok)

    if status == 403 and err_msg and "Resource not accessible by personal access token" in err_msg:
        cred_tok = get_git_credential_token()
        if cred_tok and cred_tok != tok:
            status, data, err_msg = github_api_request(url, method="GET", token=cred_tok)

    if status != 200:
        return [f"HTTP Error {status} al consultar ajustes del repositorio: {err_msg or 'Respuesta inválida'}"]

    if not isinstance(data, dict):
        return ["Respuesta del repositorio remota no es un objeto JSON válido"]

    return compare_repo_settings_dicts(data, expected_config)


def verify_protection(
    owner: str,
    repo: str,
    branch: str,
    expected_config: dict[str, Any],
    token: str | None = None,
    api_base_url: str = "https://api.github.com",
) -> list[str]:
    """Audita las reglas de protección activas de una rama contra expected_config
    conforme a la firma y contrato de SPEC-007 plan.md.
    """
    tok = get_github_token(token)
    url = f"{api_base_url.rstrip('/')}/repos/{owner}/{repo}/branches/{branch}/protection"
    status, data, err_msg = github_api_request(url, method="GET", token=tok)

    active_tok = tok
    if status == 403 and err_msg and "Resource not accessible by personal access token" in err_msg:
        cred_tok = get_git_credential_token()
        if cred_tok and cred_tok != tok:
            active_tok = cred_tok
            status, data, err_msg = github_api_request(url, method="GET", token=active_tok)

    if status == 404:
        return [f"La rama '{branch}' no tiene protección habilitada o no existe (HTTP 404: {err_msg})"]

    if status != 200:
        return [f"HTTP Error {status} al consultar protección de rama '{branch}': {err_msg or 'Respuesta inválida'}"]

    if not isinstance(data, dict):
        return [f"Respuesta de protección para rama '{branch}' no es un objeto JSON válido"]

    # Detectar si el repositorio pertenece a una cuenta de usuario personal (User)
    is_user_repo = False
    repo_url = f"{api_base_url.rstrip('/')}/repos/{owner}/{repo}"
    r_status, r_data, _ = github_api_request(repo_url, method="GET", token=active_tok)
    if r_status == 200 and isinstance(r_data, dict):
        owner_type = r_data.get("owner", {}).get("type")
        if owner_type == "User":
            is_user_repo = True

    return compare_protection_dicts(data, expected_config, is_user_repo=is_user_repo)


def load_json_file(path: Path | str) -> dict[str, Any]:
    """Carga un archivo JSON retornando su diccionario."""
    p = Path(path)
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def build_arg_parser() -> argparse.ArgumentParser:
    """Construye el analizador de argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Auditor y validador determinista de protección de ramas y ajustes de repositorio en GitHub."
    )
    parser.add_argument(
        "--owner",
        help="Propietario del repositorio en GitHub (detectado automáticamente por defecto).",
    )
    parser.add_argument(
        "--repo",
        help="Nombre del repositorio en GitHub (detectado automáticamente por defecto).",
    )
    parser.add_argument(
        "--token",
        help="Token de acceso personal o de GitHub (por defecto de GITHUB_PERSONAL_ACCESS_TOKEN o GITHUB_TOKEN).",
    )
    parser.add_argument(
        "--rules-dir",
        default="tools/git/protection_rules",
        help="Directorio con especificaciones declarativas JSON (por defecto: tools/git/protection_rules).",
    )
    parser.add_argument(
        "--branch",
        choices=["main", "dev"],
        help="Verificar una única rama protegida específica (main o dev).",
    )
    parser.add_argument(
        "--repo-only",
        action="store_true",
        help="Verificar únicamente los ajustes del repositorio (métodos de fusión).",
    )
    parser.add_argument(
        "--branches-only",
        action="store_true",
        help="Verificar únicamente las reglas de protección de ramas.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Imprimir los resultados en formato JSON.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada CLI para la verificación remota."""
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    # 1. Resolver propietario y repositorio
    owner = args.owner
    repo = args.repo
    if not owner or not repo:
        detected_owner, detected_repo = get_repo_owner_and_name()
        owner = owner or detected_owner
        repo = repo or detected_repo

    if not owner or not repo:
        sys.stderr.write(
            "Error: No se pudo determinar el propietario o repositorio. Especifique --owner y --repo.\n"
        )
        return 2

    # 2. Resolver token
    token = get_github_token(args.token)
    if not token:
        sys.stderr.write(
            "Error: Token de GitHub no encontrado. Configure GITHUB_PERSONAL_ACCESS_TOKEN, GITHUB_TOKEN o use --token.\n"
        )
        return 2

    rules_dir = Path(args.rules_dir)
    results: dict[str, Any] = {
        "owner": owner,
        "repo": repo,
        "status": "PASS",
        "discrepancies": {},
        "errors": [],
    }

    total_discrepancies = 0
    had_error = False

    # 3. Verificar ajustes de repositorio
    if not args.branches_only:
        repo_json_path = rules_dir / "repo_settings.json"
        if not repo_json_path.exists():
            msg = f"Archivo de especificación de repositorio no encontrado: {repo_json_path}"
            results["errors"].append(msg)
            had_error = True
        else:
            try:
                expected_repo = load_json_file(repo_json_path)
                disc = verify_repo_settings(owner, repo, expected_repo, token=token)
                if any(d.startswith("HTTP Error") for d in disc):
                    results["errors"].extend(disc)
                    had_error = True
                else:
                    results["discrepancies"]["repo_settings"] = disc
                    total_discrepancies += len(disc)
            except Exception as ex:
                results["errors"].append(f"Fallo al procesar {repo_json_path}: {ex}")
                had_error = True

    # 4. Verificar ramas
    if not args.repo_only:
        target_branches = [args.branch] if args.branch else ["main", "dev"]
        for b in target_branches:
            branch_json_path = rules_dir / f"{b}.json"
            if not branch_json_path.exists():
                msg = f"Archivo de especificación para rama '{b}' no encontrado: {branch_json_path}"
                results["errors"].append(msg)
                had_error = True
                continue
            try:
                expected_branch = load_json_file(branch_json_path)
                disc = verify_protection(owner, repo, b, expected_branch, token=token)
                if any(d.startswith("HTTP Error") for d in disc):
                    results["errors"].extend(disc)
                    had_error = True
                else:
                    results["discrepancies"][f"branch_{b}"] = disc
                    total_discrepancies += len(disc)
            except Exception as ex:
                results["errors"].append(f"Fallo al procesar {branch_json_path}: {ex}")
                had_error = True

    if had_error:
        results["status"] = "ERROR"
    elif total_discrepancies > 0:
        results["status"] = "FAIL"

    # Salida JSON
    if args.json_output:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        if had_error:
            return 2
        return 1 if total_discrepancies > 0 else 0

    # Salida de texto legible
    print(f"=== Auditoría de Protección de Ramas: {owner}/{repo} ===")
    if results["errors"]:
        print("\n[ERRORES DE CONECTIVIDAD O ACCESO]")
        for err in results["errors"]:
            print(f"  ! {err}")

    if results["discrepancies"]:
        for target, disc_list in results["discrepancies"].items():
            if not disc_list:
                print(f"\n[OK] {target}: Convergencia plena con la especificación.")
            else:
                print(f"\n[DESVÍO] {target}: {len(disc_list)} discrepancia(s) detectada(s):")
                for d in disc_list:
                    print(f"  - {d}")

    if had_error:
        print("\nResultado final: ERROR (código 2)")
        return 2
    if total_discrepancies > 0:
        print(f"\nResultado final: DESVÍO DETECTADO ({total_discrepancies} diferencias, código 1)")
        return 1

    print("\nResultado final: CONVERGENCIA PLENA (código 0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
