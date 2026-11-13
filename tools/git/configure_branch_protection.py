#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/git/configure_branch_protection.py

Aprovisionador determinista de configuración remota en GitHub.
Aplica ajustes del repositorio (PATCH /repos/:owner/:repo) y reglas clásicas
de protección de ramas (PUT /repos/:owner/:repo/branches/:b/protection)
consumiendo especificaciones declarativas JSON desde tools/git/protection_rules/.

Códigos de salida:
  0: Configuración aplicada exitosamente.
  1: Error al aplicar configuración remota en GitHub.
  2: Error de autenticación, argumentos o invocación.
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
        "User-Agent": "LLaMA-Branch-Protection-Configurator",
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


def load_json_file(path: Path | str) -> dict[str, Any]:
    """Carga un archivo JSON retornando su diccionario."""
    p = Path(path)
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def configure_repo_settings(
    owner: str,
    repo: str,
    settings: dict[str, Any],
    token: str | None = None,
    api_base_url: str = "https://api.github.com",
) -> tuple[bool, str]:
    """Aplica los ajustes de repositorio en GitHub vía PATCH /repos/:owner/:repo."""
    tok = get_github_token(token)
    if not tok:
        return False, "Token de GitHub no provisto ni detectado"

    url = f"{api_base_url.rstrip('/')}/repos/{owner}/{repo}"
    status, _, err_msg = github_api_request(url, method="PATCH", data=settings, token=tok)

    if status == 403 and err_msg and "Resource not accessible by personal access token" in err_msg:
        cred_tok = get_git_credential_token()
        if cred_tok and cred_tok != tok:
            status, _, err_msg = github_api_request(url, method="PATCH", data=settings, token=cred_tok)

    if status == 200:
        return True, f"Ajustes de repositorio para '{owner}/{repo}' actualizados exitosamente."

    return False, f"Fallo al actualizar ajustes de repositorio (HTTP {status}): {err_msg or 'Error desconocido'}"


def configure_branch_protection(
    owner: str,
    repo: str,
    branch: str,
    protection_config: dict[str, Any],
    token: str | None = None,
    api_base_url: str = "https://api.github.com",
) -> tuple[bool, str]:
    """Aplica las reglas de protección de rama vía PUT /repos/:owner/:repo/branches/:branch/protection."""
    tok = get_github_token(token)
    if not tok:
        return False, "Token de GitHub no provisto ni detectado"

    url = f"{api_base_url.rstrip('/')}/repos/{owner}/{repo}/branches/{branch}/protection"
    status, _, err_msg = github_api_request(
        url, method="PUT", data=protection_config, token=tok
    )

    active_tok = tok
    if status == 403 and err_msg and "Resource not accessible by personal access token" in err_msg:
        cred_tok = get_git_credential_token()
        if cred_tok and cred_tok != tok:
            active_tok = cred_tok
            status, _, err_msg = github_api_request(
                url, method="PUT", data=protection_config, token=active_tok
            )

    # En cuentas de usuario personales (User), GitHub API rechaza el objeto restrictions con HTTP 422:
    # "Only organization repositories can have users and team restrictions".
    # En cuentas personales, el bloqueo contra envíos directos fuera de PR se garantiza
    # deterministamente mediante required_pull_request_reviews y enforce_admins: true con restrictions: null.
    if status == 422 and err_msg and "Only organization repositories can have users and team restrictions" in err_msg:
        cfg = dict(protection_config)
        cfg["restrictions"] = None
        status, _, err_msg = github_api_request(
            url, method="PUT", data=cfg, token=active_tok
        )

    if status == 200:
        return True, f"Protección de rama '{branch}' configurada exitosamente."

    return False, f"Fallo al configurar protección en rama '{branch}' (HTTP {status}): {err_msg or 'Error desconocido'}"


def build_arg_parser() -> argparse.ArgumentParser:
    """Construye el analizador de argumentos y subcomandos."""
    parser = argparse.ArgumentParser(
        description="Aprovisionador determinista de protección de ramas y ajustes de repositorio en GitHub."
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

    subparsers = parser.add_subparsers(
        dest="command",
        help="Comando de aprovisionamiento a ejecutar.",
    )

    # Subcomando repo-settings
    p_repo = subparsers.add_parser(
        "repo-settings",
        help="Aplica los ajustes de métodos de fusión al repositorio.",
    )
    p_repo.add_argument(
        "--file",
        default="tools/git/protection_rules/repo_settings.json",
        help="Ruta al archivo JSON de ajustes (por defecto: tools/git/protection_rules/repo_settings.json).",
    )
    p_repo.add_argument(
        "--token",
        help="Token de acceso personal o de GitHub.",
    )

    # Subcomando branch
    p_branch = subparsers.add_parser(
        "branch",
        help="Aplica las reglas de protección a una rama específica.",
    )
    p_branch.add_argument(
        "--branch",
        required=True,
        choices=["main", "dev"],
        help="Nombre de la rama protegida (main o dev).",
    )
    p_branch.add_argument(
        "--file",
        "--rule-file",
        dest="file",
        help="Ruta al archivo JSON de reglas (por defecto: tools/git/protection_rules/<rama>.json).",
    )
    p_branch.add_argument(
        "--token",
        help="Token de acceso personal o de GitHub.",
    )

    # Subcomando all
    p_all = subparsers.add_parser(
        "all",
        help="Aplica ajustes de repositorio y protección completa a ramas main y dev.",
    )
    p_all.add_argument(
        "--rules-dir",
        default="tools/git/protection_rules",
        help="Directorio con especificaciones declarativas JSON.",
    )
    p_all.add_argument(
        "--token",
        help="Token de acceso personal o de GitHub.",
    )

    # Flags globales de conveniencia directa sin subcomando
    parser.add_argument(
        "--apply-repo-settings",
        action="store_true",
        help="Aplica repo_settings.json al repositorio.",
    )
    parser.add_argument(
        "--branch",
        dest="flag_branch",
        choices=["main", "dev"],
        help="Rama a proteger usando flags de nivel superior.",
    )
    parser.add_argument(
        "--rule-file",
        help="Archivo JSON de reglas a aplicar con --branch.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Aplica ajustes de repositorio y protección a main y dev.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada CLI para la configuración de protección."""
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    # Resolver propietario y repositorio
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

    token = get_github_token(args.token)
    if not token:
        sys.stderr.write(
            "Error: Token de GitHub no encontrado. Configure GITHUB_PERSONAL_ACCESS_TOKEN, GITHUB_TOKEN o use --token.\n"
        )
        return 2

    # Normalizar acción a ejecutar
    cmd = args.command
    if not cmd:
        if args.all:
            cmd = "all"
        elif args.apply_repo_settings:
            cmd = "repo-settings"
        elif args.flag_branch:
            cmd = "branch"
        else:
            parser.print_help()
            return 0

    success = True

    if cmd == "repo-settings":
        file_path = getattr(args, "file", None) or "tools/git/protection_rules/repo_settings.json"
        p = Path(file_path)
        if not p.exists():
            sys.stderr.write(f"Error: Archivo de especificación no encontrado: {p}\n")
            return 2
        try:
            settings = load_json_file(p)
            ok, msg = configure_repo_settings(owner, repo, settings, token=token)
            print(msg)
            if not ok:
                success = False
        except Exception as ex:
            sys.stderr.write(f"Error al procesar {p}: {ex}\n")
            return 1

    elif cmd == "branch":
        branch_name = getattr(args, "branch", None) or getattr(args, "flag_branch", None)
        file_path = getattr(args, "file", None) or getattr(args, "rule_file", None)
        if not file_path:
            file_path = f"tools/git/protection_rules/{branch_name}.json"

        p = Path(file_path)
        if not p.exists():
            sys.stderr.write(f"Error: Archivo de especificación no encontrado: {p}\n")
            return 2
        try:
            config = load_json_file(p)
            ok, msg = configure_branch_protection(owner, repo, branch_name, config, token=token)
            print(msg)
            if not ok:
                success = False
        except Exception as ex:
            sys.stderr.write(f"Error al procesar {p}: {ex}\n")
            return 1

    elif cmd == "all":
        rules_dir = Path(getattr(args, "rules_dir", "tools/git/protection_rules"))

        # 1. repo_settings
        repo_file = rules_dir / "repo_settings.json"
        if repo_file.exists():
            try:
                settings = load_json_file(repo_file)
                ok, msg = configure_repo_settings(owner, repo, settings, token=token)
                print(msg)
                if not ok:
                    success = False
            except Exception as ex:
                sys.stderr.write(f"Error al procesar {repo_file}: {ex}\n")
                success = False
        else:
            sys.stderr.write(f"Error: No se encontró {repo_file}\n")
            success = False

        # 2. branches main y dev
        for b in ["main", "dev"]:
            b_file = rules_dir / f"{b}.json"
            if b_file.exists():
                try:
                    b_cfg = load_json_file(b_file)
                    ok, msg = configure_branch_protection(owner, repo, b, b_cfg, token=token)
                    print(msg)
                    if not ok:
                        success = False
                except Exception as ex:
                    sys.stderr.write(f"Error al procesar {b_file}: {ex}\n")
                    success = False
            else:
                sys.stderr.write(f"Error: No se encontró {b_file}\n")
                success = False

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
