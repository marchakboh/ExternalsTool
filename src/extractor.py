import shutil
import zipfile
import tarfile
import subprocess
import sys
from pathlib import Path


def extract(archive_path: Path, dest_dir: Path, log_callback) -> bool:
    """
    Extract an archive into dest_dir.
    Format is detected by file extension — no guessing.

    Supported: .zip, .tar, .tar.gz, .tgz, .tar.bz2, .rar
    Returns True on success, False on failure.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    name = archive_path.name.lower()

    try:
        if name.endswith(".zip"):
            _extract_zip(archive_path, dest_dir, log_callback)

        elif name.endswith((".tar.gz", ".tgz")):
            _extract_tar(archive_path, dest_dir, log_callback, mode="r:gz")

        elif name.endswith(".tar.bz2"):
            _extract_tar(archive_path, dest_dir, log_callback, mode="r:bz2")

        elif name.endswith(".tar"):
            _extract_tar(archive_path, dest_dir, log_callback, mode="r:")

        elif name.endswith(".rar"):
            _extract_rar(archive_path, dest_dir, log_callback)

        else:
            log_callback(f"  [Extract] Unknown format: {archive_path.name}")
            return False

        return True

    except Exception as e:
        log_callback(f"  [Extract] ERROR: {e}")
        return False


# ── format handlers ──────────────────────────────────────────────────

def _extract_zip(archive: Path, dest: Path, log_callback):
    log_callback(f"  [Extract] Unzipping {archive.name}")
    with zipfile.ZipFile(archive, "r") as zf:
        zf.extractall(dest)


def _extract_tar(archive: Path, dest: Path, log_callback, mode: str = "r:"):
    log_callback(f"  [Extract] Untarring {archive.name}")
    with tarfile.open(archive, mode) as tf:
        tf.extractall(dest)


def _extract_rar(archive: Path, dest: Path, log_callback):
    """
    RAR extraction via unrar CLI.
    unrar must be installed separately (not bundled — closed-source tool).
    """
    log_callback(f"  [Extract] Unraring {archive.name} (requires 'unrar' in PATH)")

    try:
        result = subprocess.run(
            ["unrar", "x", "-o+", str(archive), str(dest)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            log_callback(f"  [Extract] unrar error: {result.stderr.strip()}")
            raise RuntimeError(f"unrar exited with code {result.returncode}")

    except FileNotFoundError:
        raise RuntimeError(
            "'unrar' not found in PATH. "
            "Install it: https://www.win-rar.com/unrarfree.html"
        )
