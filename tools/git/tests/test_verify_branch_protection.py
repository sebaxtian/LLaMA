#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/git/tests/test_verify_branch_protection.py

Suite exhaustiva de pruebas unitarias para tools/git/verify_branch_protection.py.
Cubre comparación de repo_settings, protección de ramas, detección de credenciales,
comunicación con la API REST mockeada y opciones de salida CLI/JSON.
"""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import MagicMock, patch

# Asegurar importación de verify_branch_protection
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

import tools.git.verify_branch_protection as vbp


class TestCompareRepoSettings(unittest.TestCase):
    """Pruebas unitarias para la función compare_repo_settings_dicts."""

    def setUp(self):
        self.expected = {
            "allow_merge_commit": True,
            "allow_squash_merge": False,
            "allow_rebase_merge": False,
            "delete_branch_on_merge": True,
            "allow_auto_merge": False,
        }

    def test_repo_settings_identical(self):
        """Caso idéntico: 0 discrepancias."""
        actual = dict(self.expected)
        diffs = vbp.compare_repo_settings_dicts(actual, self.expected)
        self.assertEqual(diffs, [])

    def test_repo_settings_squash_divergence(self):
        """Desvío en allow_squash_merge -> detecta discrepancia."""
        actual = dict(self.expected)
        actual["allow_squash_merge"] = True
        diffs = vbp.compare_repo_settings_dicts(actual, self.expected)
        self.assertEqual(len(diffs), 1)
        self.assertIn("allow_squash_merge", diffs[0])
        self.assertIn("esperado=False", diffs[0])
        self.assertIn("actual=True", diffs[0])

    def test_repo_settings_rebase_divergence(self):
        """Desvío en allow_rebase_merge -> detecta discrepancia."""
        actual = dict(self.expected)
        actual["allow_rebase_merge"] = True
        diffs = vbp.compare_repo_settings_dicts(actual, self.expected)
        self.assertEqual(len(diffs), 1)
        self.assertIn("allow_rebase_merge", diffs[0])
        self.assertIn("esperado=False", diffs[0])
        self.assertIn("actual=True", diffs[0])

    def test_repo_settings_merge_commit_divergence(self):
        """Desvío en allow_merge_commit -> detecta discrepancia."""
        actual = dict(self.expected)
        actual["allow_merge_commit"] = False
        diffs = vbp.compare_repo_settings_dicts(actual, self.expected)
        self.assertEqual(len(diffs), 1)
        self.assertIn("allow_merge_commit", diffs[0])
        self.assertIn("esperado=True", diffs[0])
        self.assertIn("actual=False", diffs[0])

    def test_repo_settings_missing_field(self):
        """Campo faltante en respuesta real -> detecta discrepancia (actual=None)."""
        actual = {
            "allow_merge_commit": True,
            # allow_squash_merge y allow_rebase_merge ausentes
        }
        diffs = vbp.compare_repo_settings_dicts(actual, self.expected)
        self.assertEqual(len(diffs), 4)  # squash, rebase, delete_branch_on_merge, allow_auto_merge
        self.assertTrue(any("allow_squash_merge" in d for d in diffs))
        self.assertTrue(any("allow_rebase_merge" in d for d in diffs))

    def test_repo_settings_optional_fields_divergence(self):
        """Desvíos en campos complementarios delete_branch_on_merge o allow_auto_merge."""
        actual = dict(self.expected)
        actual["delete_branch_on_merge"] = False
        diffs = vbp.compare_repo_settings_dicts(actual, self.expected)
        self.assertEqual(len(diffs), 1)
        self.assertIn("delete_branch_on_merge", diffs[0])


class TestCompareProtectionDicts(unittest.TestCase):
    """Pruebas unitarias para la función compare_protection_dicts."""

    def setUp(self):
        self.expected = {
            "enforce_admins": True,
            "required_pull_request_reviews": {
                "dismiss_stale_reviews": True,
                "require_code_owner_reviews": False,
                "required_approving_review_count": 0,
                "require_last_push_approval": False,
            },
            "restrictions": {
                "users": [],
                "teams": [],
                "apps": [],
            },
            "allow_force_pushes": False,
            "allow_deletions": False,
            "block_creations": False,
            "required_conversation_resolution": False,
            "required_linear_history": False,
            "required_status_checks": None,
        }

    def test_protection_identical_with_extracted_enabled(self):
        """Caso idéntico devuelto por GitHub API con envoltorios {'enabled': bool} -> 0 diferencias."""
        actual = {
            "enforce_admins": {"enabled": True, "url": "https://api.github.com/..."},
            "required_pull_request_reviews": {
                "dismiss_stale_reviews": True,
                "require_code_owner_reviews": False,
                "required_approving_review_count": 0,
                "require_last_push_approval": False,
            },
            "restrictions": {
                "users": [],
                "teams": [],
                "apps": [],
            },
            "allow_force_pushes": {"enabled": False},
            "allow_deletions": {"enabled": False},
            "block_creations": {"enabled": False},
            "required_conversation_resolution": {"enabled": False},
            "required_linear_history": {"enabled": False},
            "required_status_checks": None,
        }
        diffs = vbp.compare_protection_dicts(actual, self.expected)
        self.assertEqual(diffs, [])

    def test_enforce_admins_mismatch(self):
        """Desvío en enforce_admins (False vs True) -> detecta discrepancia."""
        actual = {
            "enforce_admins": {"enabled": False},
            "required_pull_request_reviews": self.expected["required_pull_request_reviews"],
            "restrictions": self.expected["restrictions"],
            "allow_force_pushes": False,
            "allow_deletions": False,
        }
        diffs = vbp.compare_protection_dicts(actual, self.expected)
        self.assertTrue(any("enforce_admins: esperado=True, actual=False" in d for d in diffs))

    def test_allow_force_pushes_mismatch(self):
        """Desvío en allow_force_pushes (True vs False) -> detecta discrepancia."""
        actual = {
            "enforce_admins": True,
            "required_pull_request_reviews": self.expected["required_pull_request_reviews"],
            "restrictions": self.expected["restrictions"],
            "allow_force_pushes": {"enabled": True},
            "allow_deletions": False,
        }
        diffs = vbp.compare_protection_dicts(actual, self.expected)
        self.assertTrue(any("allow_force_pushes: esperado=False, actual=True" in d for d in diffs))

    def test_allow_deletions_mismatch(self):
        """Desvío en allow_deletions (True vs False) -> detecta discrepancia."""
        actual = {
            "enforce_admins": True,
            "required_pull_request_reviews": self.expected["required_pull_request_reviews"],
            "restrictions": self.expected["restrictions"],
            "allow_force_pushes": False,
            "allow_deletions": True,
        }
        diffs = vbp.compare_protection_dicts(actual, self.expected)
        self.assertTrue(any("allow_deletions: esperado=False, actual=True" in d for d in diffs))

    def test_required_approving_review_count_mismatch(self):
        """Desvío en required_approving_review_count (1 vs 0) -> detecta discrepancia."""
        actual = {
            "enforce_admins": True,
            "required_pull_request_reviews": {
                "dismiss_stale_reviews": True,
                "require_code_owner_reviews": False,
                "required_approving_review_count": 1,
                "require_last_push_approval": False,
            },
            "restrictions": self.expected["restrictions"],
            "allow_force_pushes": False,
            "allow_deletions": False,
        }
        diffs = vbp.compare_protection_dicts(actual, self.expected)
        self.assertTrue(
            any(
                "required_pull_request_reviews.required_approving_review_count: esperado=0, actual=1"
                in d
                for d in diffs
            )
        )

    def test_required_pull_request_reviews_null_when_expected(self):
        """Si required_pull_request_reviews es None pero se esperaba dict -> detecta discrepancia."""
        actual = {
            "enforce_admins": True,
            "required_pull_request_reviews": None,
            "restrictions": self.expected["restrictions"],
            "allow_force_pushes": False,
            "allow_deletions": False,
        }
        diffs = vbp.compare_protection_dicts(actual, self.expected)
        self.assertTrue(any("required_pull_request_reviews: esperado configurado" in d for d in diffs))

    def test_required_conversation_resolution_mismatch(self):
        """Desvío en required_conversation_resolution -> detecta discrepancia."""
        expected = dict(self.expected)
        expected["required_conversation_resolution"] = True
        actual = {
            "enforce_admins": True,
            "required_pull_request_reviews": self.expected["required_pull_request_reviews"],
            "restrictions": self.expected["restrictions"],
            "allow_force_pushes": False,
            "allow_deletions": False,
            "required_conversation_resolution": False,
        }
        diffs = vbp.compare_protection_dicts(actual, expected)
        self.assertTrue(
            any(
                "required_conversation_resolution: esperado=True, actual=False" in d
                for d in diffs
            )
        )

    def test_restrictions_null_when_expected(self):
        """restrictions desactivada (None) cuando se esperaba objeto con listas -> detecta discrepancia."""
        actual = {
            "enforce_admins": True,
            "required_pull_request_reviews": self.expected["required_pull_request_reviews"],
            "restrictions": None,
            "allow_force_pushes": False,
            "allow_deletions": False,
        }
        diffs = vbp.compare_protection_dicts(actual, self.expected)
        self.assertTrue(any("restrictions: esperado configurado" in d for d in diffs))

    def test_restrictions_users_teams_apps_differ(self):
        """restrictions con usuarios, equipos o aplicaciones inesperadas -> detecta discrepancia."""
        actual = {
            "enforce_admins": True,
            "required_pull_request_reviews": self.expected["required_pull_request_reviews"],
            "restrictions": {
                "users": [{"login": "unexpected_user"}],
                "teams": [{"slug": "devs"}],
                "apps": [{"slug": "bot"}],
            },
            "allow_force_pushes": False,
            "allow_deletions": False,
        }
        diffs = vbp.compare_protection_dicts(actual, self.expected)
        self.assertTrue(any("restrictions.users:" in d for d in diffs))
        self.assertTrue(any("restrictions.teams:" in d for d in diffs))
        self.assertTrue(any("restrictions.apps:" in d for d in diffs))

    def test_required_status_checks_unexpected_checks(self):
        """expected required_status_checks=None pero actual tiene checks activos -> detecta discrepancia."""
        actual = {
            "enforce_admins": True,
            "required_pull_request_reviews": self.expected["required_pull_request_reviews"],
            "restrictions": self.expected["restrictions"],
            "allow_force_pushes": False,
            "allow_deletions": False,
            "required_status_checks": {"checks": [{"context": "ci/test"}]},
        }
        diffs = vbp.compare_protection_dicts(actual, self.expected)
        self.assertTrue(any("required_status_checks: esperado=None" in d for d in diffs))


class TestTokenAndRemoteDetection(unittest.TestCase):
    """Pruebas unitarias para resolución de token y detección de remoto git."""

    def test_get_github_token_cli_override(self):
        """El parámetro cli_token tiene la máxima precedencia."""
        with patch.dict(os.environ, {"GITHUB_TOKEN": "env_token"}):
            tok = vbp.get_github_token("cli_explicit_token")
            self.assertEqual(tok, "cli_explicit_token")

    def test_get_github_token_env_precedence(self):
        """Precedencia de variables de entorno: GITHUB_PERSONAL_ACCESS_TOKEN > GITHUB_TOKEN > GH_TOKEN."""
        with patch.dict(
            os.environ,
            {
                "GITHUB_PERSONAL_ACCESS_TOKEN": "token_pat",
                "GITHUB_TOKEN": "token_gh",
                "GH_TOKEN": "token_short",
            },
            clear=True,
        ):
            self.assertEqual(vbp.get_github_token(), "token_pat")

        with patch.dict(
            os.environ,
            {
                "GITHUB_TOKEN": "token_gh",
                "GH_TOKEN": "token_short",
            },
            clear=True,
        ):
            self.assertEqual(vbp.get_github_token(), "token_gh")

        with patch.dict(
            os.environ,
            {
                "GH_TOKEN": "token_short",
            },
            clear=True,
        ):
            self.assertEqual(vbp.get_github_token(), "token_short")

    @patch("subprocess.run")
    def test_get_github_token_gh_cli_fallback(self, mock_run):
        """Fallback a `gh auth token` si no hay env vars ni CLI token."""
        with patch.dict(os.environ, {}, clear=True):
            mock_run.return_value = subprocess.CompletedProcess(
                args=["gh", "auth", "token"],
                returncode=0,
                stdout="gh_cli_token_123\n",
                stderr="",
            )
            tok = vbp.get_github_token()
            self.assertEqual(tok, "gh_cli_token_123")
            mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_get_github_token_none_when_unavailable(self, mock_run):
        """Retorna None si ninguna fuente provee token."""
        with patch.dict(os.environ, {}, clear=True):
            mock_run.side_effect = FileNotFoundError("gh no existe")
            tok = vbp.get_github_token()
            self.assertIsNone(tok)

    @patch("subprocess.run")
    def test_get_repo_owner_and_name_https(self, mock_run):
        """Detección correcta desde URL HTTPS con o sin .git."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=["git", "remote", "get-url", "origin"],
            returncode=0,
            stdout="https://github.com/sebaxtian/LLaMA.git\n",
            stderr="",
        )
        owner, repo = vbp.get_repo_owner_and_name()
        self.assertEqual(owner, "sebaxtian")
        self.assertEqual(repo, "LLaMA")

    @patch("subprocess.run")
    def test_get_repo_owner_and_name_ssh(self, mock_run):
        """Detección correcta desde URL SSH."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=["git", "remote", "get-url", "origin"],
            returncode=0,
            stdout="git@github.com:myorg/myrepo.git\n",
            stderr="",
        )
        owner, repo = vbp.get_repo_owner_and_name()
        self.assertEqual(owner, "myorg")
        self.assertEqual(repo, "myrepo")

    @patch("subprocess.run")
    def test_get_repo_owner_and_name_error(self, mock_run):
        """Retorna (None, None) ante fallo de git."""
        mock_run.side_effect = subprocess.SubprocessError("git error")
        owner, repo = vbp.get_repo_owner_and_name()
        self.assertIsNone(owner)
        self.assertIsNone(repo)


class TestApiRequestsAndVerification(unittest.TestCase):
    """Pruebas unitarias para github_api_request, verify_repo_settings y verify_protection."""

    @patch("urllib.request.urlopen")
    def test_github_api_request_success(self, mock_urlopen):
        """Petición GET exitosa retorna status 200 y JSON decodificado."""
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = b'{"name": "test-repo", "allow_merge_commit": true}'
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        status, data, err = vbp.github_api_request("https://api.github.com/repos/owner/repo")
        self.assertEqual(status, 200)
        self.assertEqual(data.get("name"), "test-repo")
        self.assertIsNone(err)

    @patch("urllib.request.urlopen")
    def test_github_api_request_http_error(self, mock_urlopen):
        """Petición con HTTPError (404 Not Found) retorna código y mensaje de error."""
        err_stream = io.BytesIO(b'{"message": "Branch not protected"}')
        http_err = urllib.error.HTTPError(
            url="https://api.github.com",
            code=404,
            msg="Not Found",
            hdrs={},
            fp=err_stream,
        )
        mock_urlopen.side_effect = http_err

        status, data, err = vbp.github_api_request("https://api.github.com/repos/owner/repo")
        http_err.close()
        self.assertEqual(status, 404)
        self.assertEqual(err, "Branch not protected")

    @patch("urllib.request.urlopen")
    def test_github_api_request_url_error(self, mock_urlopen):
        """Petición con URLError (fallo de red) retorna status 0 y mensaje."""
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

        status, data, err = vbp.github_api_request("https://api.github.com/repos/owner/repo")
        self.assertEqual(status, 0)
        self.assertIn("Error de red", err)

    @patch("tools.git.verify_branch_protection.github_api_request")
    def test_verify_repo_settings_converged(self, mock_api):
        """verify_repo_settings retorna lista vacía cuando los ajustes son idénticos."""
        mock_api.return_value = (
            200,
            {
                "allow_merge_commit": True,
                "allow_squash_merge": False,
                "allow_rebase_merge": False,
            },
            None,
        )
        discrepancies = vbp.verify_repo_settings("owner", "repo", token="dummy")
        self.assertEqual(discrepancies, [])

    @patch("tools.git.verify_branch_protection.github_api_request")
    def test_verify_repo_settings_http_failure(self, mock_api):
        """verify_repo_settings reporta error HTTP cuando status != 200."""
        mock_api.return_value = (403, None, "API rate limit exceeded")
        discrepancies = vbp.verify_repo_settings("owner", "repo", token="dummy")
        self.assertEqual(len(discrepancies), 1)
        self.assertTrue(discrepancies[0].startswith("HTTP Error 403"))

    @patch("tools.git.verify_branch_protection.github_api_request")
    def test_verify_protection_converged(self, mock_api):
        """verify_protection retorna lista vacía cuando la regla coincide plenamente."""
        expected = {
            "enforce_admins": True,
            "allow_force_pushes": False,
            "allow_deletions": False,
            "required_pull_request_reviews": {
                "required_approving_review_count": 0,
                "dismiss_stale_reviews": True,
            },
        }
        mock_api.return_value = (
            200,
            {
                "enforce_admins": {"enabled": True},
                "allow_force_pushes": {"enabled": False},
                "allow_deletions": {"enabled": False},
                "required_pull_request_reviews": {
                    "required_approving_review_count": 0,
                    "dismiss_stale_reviews": True,
                },
            },
            None,
        )
        discrepancies = vbp.verify_protection("owner", "repo", "main", expected, token="dummy")
        self.assertEqual(discrepancies, [])

    @patch("tools.git.verify_branch_protection.github_api_request")
    def test_verify_protection_branch_not_protected_404(self, mock_api):
        """verify_protection detecta cuando una rama no tiene protección (HTTP 404)."""
        mock_api.return_value = (404, None, "Branch not protected")
        discrepancies = vbp.verify_protection("owner", "repo", "main", {}, token="dummy")
        self.assertEqual(len(discrepancies), 1)
        self.assertIn("no tiene protección habilitada", discrepancies[0])


class TestMainCliExecution(unittest.TestCase):
    """Pruebas unitarias de ejecución de la función main con salida CLI y JSON."""

    def setUp(self):
        self.rules_dir = REPO_ROOT / "tools" / "git" / "protection_rules"

    @patch("tools.git.verify_branch_protection.get_repo_owner_and_name")
    @patch("tools.git.verify_branch_protection.get_github_token")
    def test_main_missing_repo_fails_with_code_2(self, mock_token, mock_repo):
        """main retorna código 2 si no se puede detectar propietario y repositorio."""
        mock_repo.return_value = (None, None)
        mock_token.return_value = "dummy_token"

        with patch("sys.stderr", new_callable=io.StringIO):
            code = vbp.main(["--rules-dir", str(self.rules_dir)])
            self.assertEqual(code, 2)

    @patch("tools.git.verify_branch_protection.get_repo_owner_and_name")
    @patch("tools.git.verify_branch_protection.get_github_token")
    def test_main_missing_token_fails_with_code_2(self, mock_token, mock_repo):
        """main retorna código 2 si no hay token de autenticación disponible."""
        mock_repo.return_value = ("owner", "repo")
        mock_token.return_value = None

        with patch("sys.stderr", new_callable=io.StringIO):
            code = vbp.main(["--rules-dir", str(self.rules_dir)])
            self.assertEqual(code, 2)

    @patch("tools.git.verify_branch_protection.verify_protection")
    @patch("tools.git.verify_branch_protection.verify_repo_settings")
    def test_main_all_converged_json_output_returns_0(self, mock_verify_repo, mock_verify_prot):
        """main con salida JSON y sin diferencias devuelve código 0 y JSON status PASS."""
        mock_verify_repo.return_value = []
        mock_verify_prot.return_value = []

        stdout_buf = io.StringIO()
        with patch("sys.stdout", stdout_buf):
            code = vbp.main(
                [
                    "--owner",
                    "testowner",
                    "--repo",
                    "testrepo",
                    "--token",
                    "fake_tok",
                    "--rules-dir",
                    str(self.rules_dir),
                    "--json",
                ]
            )

        self.assertEqual(code, 0)
        output = json.loads(stdout_buf.getvalue())
        self.assertEqual(output["status"], "PASS")
        self.assertEqual(output["errors"], [])
        self.assertEqual(output["owner"], "testowner")
        self.assertEqual(output["repo"], "testrepo")
        self.assertEqual(output["discrepancies"]["repo_settings"], [])
        self.assertEqual(output["discrepancies"]["branch_main"], [])
        self.assertEqual(output["discrepancies"]["branch_dev"], [])

    @patch("tools.git.verify_branch_protection.verify_protection")
    @patch("tools.git.verify_branch_protection.verify_repo_settings")
    def test_main_discrepancies_detected_json_output_returns_1(
        self, mock_verify_repo, mock_verify_prot
    ):
        """main con discrepancias devuelve código 1 y status FAIL."""
        mock_verify_repo.return_value = ["Ajuste 'allow_squash_merge': esperado=False, actual=True"]
        mock_verify_prot.return_value = []

        stdout_buf = io.StringIO()
        with patch("sys.stdout", stdout_buf):
            code = vbp.main(
                [
                    "--owner",
                    "testowner",
                    "--repo",
                    "testrepo",
                    "--token",
                    "fake_tok",
                    "--rules-dir",
                    str(self.rules_dir),
                    "--json",
                ]
            )

        self.assertEqual(code, 1)
        output = json.loads(stdout_buf.getvalue())
        self.assertEqual(output["status"], "FAIL")
        self.assertEqual(len(output["discrepancies"]["repo_settings"]), 1)

    @patch("tools.git.verify_branch_protection.verify_protection")
    @patch("tools.git.verify_branch_protection.verify_repo_settings")
    def test_main_repo_only_flag(self, mock_verify_repo, mock_verify_prot):
        """main con flag --repo-only audita exclusivamente ajustes del repositorio."""
        mock_verify_repo.return_value = []

        stdout_buf = io.StringIO()
        with patch("sys.stdout", stdout_buf):
            code = vbp.main(
                [
                    "--owner",
                    "testowner",
                    "--repo",
                    "testrepo",
                    "--token",
                    "fake_tok",
                    "--rules-dir",
                    str(self.rules_dir),
                    "--repo-only",
                    "--json",
                ]
            )

        self.assertEqual(code, 0)
        output = json.loads(stdout_buf.getvalue())
        self.assertIn("repo_settings", output["discrepancies"])
        self.assertNotIn("branch_main", output["discrepancies"])
        self.assertNotIn("branch_dev", output["discrepancies"])
        mock_verify_prot.assert_not_called()

    @patch("tools.git.verify_branch_protection.verify_protection")
    @patch("tools.git.verify_branch_protection.verify_repo_settings")
    def test_main_branches_only_and_single_branch_flag(
        self, mock_verify_repo, mock_verify_prot
    ):
        """main con flag --branches-only y --branch main audita únicamente branch_main."""
        mock_verify_prot.return_value = []

        stdout_buf = io.StringIO()
        with patch("sys.stdout", stdout_buf):
            code = vbp.main(
                [
                    "--owner",
                    "testowner",
                    "--repo",
                    "testrepo",
                    "--token",
                    "fake_tok",
                    "--rules-dir",
                    str(self.rules_dir),
                    "--branches-only",
                    "--branch",
                    "main",
                    "--json",
                ]
            )

        self.assertEqual(code, 0)
        output = json.loads(stdout_buf.getvalue())
        self.assertNotIn("repo_settings", output["discrepancies"])
        self.assertIn("branch_main", output["discrepancies"])
        self.assertNotIn("branch_dev", output["discrepancies"])
        mock_verify_repo.assert_not_called()
        mock_verify_prot.assert_called_once()

    @patch("tools.git.verify_branch_protection.verify_protection")
    @patch("tools.git.verify_branch_protection.verify_repo_settings")
    def test_main_human_readable_text_output(self, mock_verify_repo, mock_verify_prot):
        """main en modo texto legible imprime resumen estructurado y retorna 0."""
        mock_verify_repo.return_value = []
        mock_verify_prot.return_value = []

        stdout_buf = io.StringIO()
        with patch("sys.stdout", stdout_buf):
            code = vbp.main(
                [
                    "--owner",
                    "testowner",
                    "--repo",
                    "testrepo",
                    "--token",
                    "fake_tok",
                    "--rules-dir",
                    str(self.rules_dir),
                ]
            )

        self.assertEqual(code, 0)
        text = stdout_buf.getvalue()
        self.assertIn("=== Auditoría de Protección de Ramas: testowner/testrepo ===", text)
        self.assertIn("Convergencia plena con la especificación", text)
        self.assertIn("CONVERGENCIA PLENA (código 0)", text)


if __name__ == "__main__":
    unittest.main()
