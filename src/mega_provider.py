import subprocess
import sys
from pathlib import Path

from base_provider import BaseProvider


class MegaProvider(BaseProvider):
    """
    Downloads assets from Mega cloud via the megatools CLI.
    megatools.exe (or megadl on Linux) must be available at the configured path.
    """

    def __init__(self, megatool_path: str | None = None):
        """
        Args:
            megatool_path: Explicit path to megatools binary.
                           If None, falls back to Tools/megatools/ relative to exe.
        """
        self._megatool_path = megatool_path or self._default_megatool_path()

    # ── interface ─────────────────────────────────────────────────────

    @property
    def name(self) -> str:
        return "Mega"

    def download(self, url: str, dest_dir: Path, log_callback) -> Path | None:
        dest_dir.mkdir(parents=True, exist_ok=True)

        command = [self._megatool_path, "dl", "--path", str(dest_dir), url]
        log_callback(f"  [Mega] Running: {' '.join(command)}")

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            for line in process.stdout:
                stripped = line.rstrip()
                if stripped:
                    log_callback(f"  [Mega] {stripped}")

            process.wait()

            if process.returncode != 0:
                stderr_output = process.stderr.read().strip()
                log_callback(f"  [Mega] ERROR (exit {process.returncode}): {stderr_output}")
                return None

        except FileNotFoundError:
            log_callback(f"  [Mega] ERROR: megatools not found at '{self._megatool_path}'")
            return None
        except Exception as e:
            log_callback(f"  [Mega] ERROR: {e}")
            return None

        # return the first file that appeared in dest_dir
        files = [f for f in dest_dir.iterdir() if f.is_file()]
        return files[0] if files else None

    # ── internals ─────────────────────────────────────────────────────

    @staticmethod
    def _default_megatool_path() -> str:
        """Resolve megatools binary relative to the running script/exe."""
        if getattr(sys, "frozen", False):
            base = Path(sys.executable).parent
        else:
            base = Path(__file__).resolve().parent.parent

        # Tools/megatools/ lives one level up from the package root
        binary = "megatools.exe" if sys.platform == "win32" else "megadl"
        return str(base.parent / "Tools" / "megatools" / binary)
