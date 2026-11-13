#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/git/tests/test_remote_rejection.py

Suite determinista de pruebas de rechazo remoto contra GitHub origin (SPEC-007 / T-009).
Verifica que las reglas de protección de las ramas 'main' y 'dev' rechazan
operaciones no autorizadas en el servidor remoto:
  1. Rechazo de push directo a 'dev' y 'main' fuera de Pull Request (RF-002, CA-001).
  2. Rechazo de push forzado con '--force' y '--force-with-lease' (RF-003, CB-001, CA-002).
  3. Rechazo de eliminación remota de 'dev' y 'main' (RF-004, CB-006, CA-003).
  4. Rechazo de commit de empaquetado release directo a 'dev' (CB-005, CA-001).
  5. Tiempo de respuesta inferior a 5 segundos por operación (RNF-002).
  6. Preservación estricta del estado local y working tree sin contaminación.
"""

from __future__ import annotations

import subprocess
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent


class TestRemoteRejection(unittest.TestCase):
    """Pruebas deterministas de rechazo remoto contra el repositorio GitHub origin."""

    remote_url: str = ""

    @classmethod
    def setUpClass(cls) -> None:
        """Verifica la disponibilidad de Git y la configuración del remoto origin."""
        res = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )
        if res.returncode != 0:
            raise unittest.SkipTest("Remoto 'origin' no configurado o inalcanzable localmente.")
        cls.remote_url = res.stdout.strip()

    def _create_temp_commit(self, parent_branch: str, message: str) -> str:
        """Crea un objeto commit aislado en el almacén git local sin alterar HEAD, index ni working tree."""
        tree = subprocess.check_output(
            ["git", "write-tree"],
            cwd=str(REPO_ROOT),
        ).decode("utf-8").strip()

        parent_rev = f"origin/{parent_branch}"
        try:
            parent_sha = subprocess.check_output(
                ["git", "rev-parse", parent_rev],
                cwd=str(REPO_ROOT),
                stderr=subprocess.DEVNULL,
            ).decode("utf-8").strip()
        except subprocess.CalledProcessError:
            parent_sha = subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=str(REPO_ROOT),
            ).decode("utf-8").strip()

        cmd = ["git", "commit-tree", tree, "-p", parent_sha, "-m", message]
        commit_sha = subprocess.check_output(
            cmd,
            cwd=str(REPO_ROOT),
        ).decode("utf-8").strip()
        return commit_sha

    def _run_git_push(self, *push_args: str) -> tuple[subprocess.CompletedProcess[str], float]:
        """Ejecuta un comando git push contra origin midiendo el tiempo de respuesta."""
        cmd = ["git", "push", "origin", *push_args]
        t0 = time.monotonic()
        proc = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )
        elapsed = time.monotonic() - t0
        return proc, elapsed

    def test_direct_push_to_dev_rejected(self) -> None:
        """Test 1: Push directo a 'dev' fuera de Pull Request es rechazado (RF-002, CA-001)."""
        commit_sha = self._create_temp_commit("dev", "test: probe direct push to dev without PR")
        proc, elapsed = self._run_git_push(f"{commit_sha}:refs/heads/dev")

        self.assertNotEqual(
            proc.returncode,
            0,
            f"El push directo a 'dev' debió fallar, pero terminó con éxito (salida: {proc.stdout})",
        )
        combined = proc.stdout + proc.stderr
        self.assertTrue(
            "GH006" in combined
            or "Protected branch update failed" in combined
            or "Changes must be made through a pull request" in combined
            or "protected branch hook declined" in combined,
            f"El mensaje de rechazo de GitHub esperado no fue encontrado en: {combined}",
        )
        self.assertLess(
            elapsed,
            5.0,
            f"El tiempo de respuesta del servidor remoto ({elapsed:.2f}s) superó los 5.0s (RNF-002)",
        )

    def test_direct_push_to_main_rejected(self) -> None:
        """Test 2: Push directo a 'main' fuera de Pull Request es rechazado (RF-002, CA-001)."""
        commit_sha = self._create_temp_commit("main", "test: probe direct push to main without PR")
        proc, elapsed = self._run_git_push(f"{commit_sha}:refs/heads/main")

        self.assertNotEqual(
            proc.returncode,
            0,
            f"El push directo a 'main' debió fallar, pero terminó con éxito (salida: {proc.stdout})",
        )
        combined = proc.stdout + proc.stderr
        self.assertTrue(
            "GH006" in combined
            or "Protected branch update failed" in combined
            or "Changes must be made through a pull request" in combined
            or "protected branch hook declined" in combined,
            f"El mensaje de rechazo de GitHub esperado no fue encontrado en: {combined}",
        )
        self.assertLess(
            elapsed,
            5.0,
            f"El tiempo de respuesta del servidor remoto ({elapsed:.2f}s) superó los 5.0s (RNF-002)",
        )

    def test_force_push_to_dev_rejected(self) -> None:
        """Test 3: Push forzado con '--force' a 'dev' es rechazado (RF-003, CA-002)."""
        commit_sha = self._create_temp_commit("dev", "test: probe force push to dev")
        proc, elapsed = self._run_git_push("--force", f"{commit_sha}:refs/heads/dev")

        self.assertNotEqual(
            proc.returncode,
            0,
            f"El push forzado a 'dev' debió ser rechazado, pero terminó con éxito (salida: {proc.stdout})",
        )
        combined = proc.stdout + proc.stderr
        self.assertTrue(
            "GH006" in combined
            or "GH003" in combined
            or "Protected branch update failed" in combined
            or "protected branch hook declined" in combined
            or "cannot force push" in combined,
            f"El mensaje de rechazo esperado no fue encontrado en: {combined}",
        )
        self.assertLess(
            elapsed,
            5.0,
            f"El tiempo de respuesta del servidor remoto ({elapsed:.2f}s) superó los 5.0s (RNF-002)",
        )

    def test_force_push_with_lease_to_dev_rejected(self) -> None:
        """Test 4: Push forzado con '--force-with-lease' a 'dev' es rechazado (RF-003, CB-001, CA-002)."""
        commit_sha = self._create_temp_commit("dev", "test: probe force-with-lease to dev")
        proc, elapsed = self._run_git_push("--force-with-lease", f"{commit_sha}:refs/heads/dev")

        self.assertNotEqual(
            proc.returncode,
            0,
            f"El push con '--force-with-lease' a 'dev' debió ser rechazado, pero terminó con éxito (salida: {proc.stdout})",
        )
        combined = proc.stdout + proc.stderr
        self.assertTrue(
            "GH006" in combined
            or "GH003" in combined
            or "Protected branch update failed" in combined
            or "protected branch hook declined" in combined
            or "cannot force push" in combined,
            f"El mensaje de rechazo esperado no fue encontrado en: {combined}",
        )
        self.assertLess(
            elapsed,
            5.0,
            f"El tiempo de respuesta del servidor remoto ({elapsed:.2f}s) superó los 5.0s (RNF-002)",
        )

    def test_force_push_to_main_rejected(self) -> None:
        """Test 5: Push forzado con '--force' a 'main' es rechazado (RF-003, CA-002)."""
        commit_sha = self._create_temp_commit("main", "test: probe force push to main")
        proc, elapsed = self._run_git_push("--force", f"{commit_sha}:refs/heads/main")

        self.assertNotEqual(
            proc.returncode,
            0,
            f"El push forzado a 'main' debió ser rechazado, pero terminó con éxito (salida: {proc.stdout})",
        )
        combined = proc.stdout + proc.stderr
        self.assertTrue(
            "GH006" in combined
            or "GH003" in combined
            or "Protected branch update failed" in combined
            or "protected branch hook declined" in combined
            or "cannot force push" in combined,
            f"El mensaje de rechazo esperado no fue encontrado en: {combined}",
        )
        self.assertLess(
            elapsed,
            5.0,
            f"El tiempo de respuesta del servidor remoto ({elapsed:.2f}s) superó los 5.0s (RNF-002)",
        )

    def test_force_push_with_lease_to_main_rejected(self) -> None:
        """Test 6: Push forzado con '--force-with-lease' a 'main' es rechazado (RF-003, CB-001, CA-002)."""
        commit_sha = self._create_temp_commit("main", "test: probe force-with-lease to main")
        proc, elapsed = self._run_git_push("--force-with-lease", f"{commit_sha}:refs/heads/main")

        self.assertNotEqual(
            proc.returncode,
            0,
            f"El push con '--force-with-lease' a 'main' debió ser rechazado, pero terminó con éxito (salida: {proc.stdout})",
        )
        combined = proc.stdout + proc.stderr
        self.assertTrue(
            "GH006" in combined
            or "GH003" in combined
            or "Protected branch update failed" in combined
            or "protected branch hook declined" in combined
            or "cannot force push" in combined,
            f"El mensaje de rechazo esperado no fue encontrado en: {combined}",
        )
        self.assertLess(
            elapsed,
            5.0,
            f"El tiempo de respuesta del servidor remoto ({elapsed:.2f}s) superó los 5.0s (RNF-002)",
        )

    def test_delete_remote_dev_rejected(self) -> None:
        """Test 7: Intento de supresión de rama remota 'dev' es rechazado (RF-004, CB-006, CA-003)."""
        proc, elapsed = self._run_git_push("--delete", "dev")

        self.assertNotEqual(
            proc.returncode,
            0,
            f"La supresión remota de 'dev' debió ser rechazada, pero terminó con éxito (salida: {proc.stdout})",
        )
        combined = proc.stdout + proc.stderr
        self.assertTrue(
            "GH006" in combined
            or "Cannot delete this branch" in combined
            or "Protected branch update failed" in combined
            or "protected branch hook declined" in combined,
            f"El mensaje de rechazo esperado no fue encontrado en: {combined}",
        )
        self.assertLess(
            elapsed,
            5.0,
            f"El tiempo de respuesta del servidor remoto ({elapsed:.2f}s) superó los 5.0s (RNF-002)",
        )

    def test_delete_remote_main_rejected(self) -> None:
        """Test 8: Intento de supresión de rama remota 'main' es rechazado (RF-004, CA-003)."""
        proc, elapsed = self._run_git_push("--delete", "main")

        self.assertNotEqual(
            proc.returncode,
            0,
            f"La supresión remota de 'main' debió ser rechazada, pero terminó con éxito (salida: {proc.stdout})",
        )
        combined = proc.stdout + proc.stderr
        self.assertTrue(
            "GH006" in combined
            or "Cannot delete this branch" in combined
            or "Protected branch update failed" in combined
            or "protected branch hook declined" in combined
            or "refusing to delete the current branch" in combined,
            f"El mensaje de rechazo esperado no fue encontrado en: {combined}",
        )
        self.assertLess(
            elapsed,
            5.0,
            f"El tiempo de respuesta del servidor remoto ({elapsed:.2f}s) superó los 5.0s (RNF-002)",
        )

    def test_direct_push_release_commit_to_dev_rejected(self) -> None:
        """Test 9: Push directo con commit 'chore: prepare release' a 'dev' es rechazado (CB-005, CA-001)."""
        commit_sha = self._create_temp_commit(
            "dev",
            "chore: prepare release v0.1.0\n\nPrueba de intento de empaquetado directo fuera de PR.",
        )
        proc, elapsed = self._run_git_push(f"{commit_sha}:refs/heads/dev")

        self.assertNotEqual(
            proc.returncode,
            0,
            f"El push directo de empaquetado a 'dev' debió fallar, pero terminó con éxito (salida: {proc.stdout})",
        )
        combined = proc.stdout + proc.stderr
        self.assertTrue(
            "GH006" in combined
            or "Protected branch update failed" in combined
            or "Changes must be made through a pull request" in combined
            or "protected branch hook declined" in combined,
            f"El mensaje de rechazo de GitHub esperado no fue encontrado en: {combined}",
        )
        self.assertLess(
            elapsed,
            5.0,
            f"El tiempo de respuesta del servidor remoto ({elapsed:.2f}s) superó los 5.0s (RNF-002)",
        )


if __name__ == "__main__":
    unittest.main()
