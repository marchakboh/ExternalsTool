import shutil
from pathlib import Path
from typing import Callable

from config import AssetEntry
from extractor import extract
import provider_registry


class SyncRunner:
    """
    Processes a list of AssetEntry sequentially:
        1. Resolve provider for each entry
        2. Download into a temp dir
        3. If the result is an archive → extract into the target location
           Otherwise → move the file directly
        4. Clean up temp dir for that entry

    All progress is reported via log_callback(str).
    """

    def __init__(self, root_dir: Path, temp_dir: Path, log_callback: Callable[[str], None]):
        self._root     = root_dir
        self._temp     = temp_dir
        self._log      = log_callback

    # ── public ────────────────────────────────────────────────────────

    def run(self, entries: list[AssetEntry]) -> None:
        """Kick off sequential sync for the given entries."""
        if not entries:
            self._log("Nothing selected.")
            return

        self._temp.mkdir(parents=True, exist_ok=True)

        for entry in entries:
            self._log(f"\n── {entry.name} ──")
            success = self._process_entry(entry)
            if not success:
                self._log(f"  ⚠ Skipped: {entry.name}")

        self._log("\nFinished.")

    # ── internals ─────────────────────────────────────────────────────

    def _process_entry(self, entry: AssetEntry) -> bool:
        # 1. resolve provider
        provider = provider_registry.get_provider(entry.type)
        if provider is None:
            self._log(f"  ERROR: Unknown provider type '{entry.type}'")
            return False

        # 2. download into a per-entry temp folder
        entry_temp = self._temp / entry.name
        if entry_temp.exists():
            shutil.rmtree(entry_temp)
        entry_temp.mkdir(parents=True)

        downloaded_file = provider.download(entry.url, entry_temp, self._log)
        if downloaded_file is None:
            self._cleanup(entry_temp)
            return False

        # 3. extract or move
        dest_dir = self._root / entry.location
        dest_dir.mkdir(parents=True, exist_ok=True)

        if _is_archive(downloaded_file):
            ok = extract(downloaded_file, dest_dir, self._log)
            if not ok:
                self._cleanup(entry_temp)
                return False
        else:
            self._log(f"  [Move] {downloaded_file.name} → {dest_dir}")
            shutil.move(str(downloaded_file), str(dest_dir / downloaded_file.name))

        # 4. cleanup
        self._cleanup(entry_temp)
        self._log(f"  ✓ Done: {entry.name}")
        return True

    @staticmethod
    def _cleanup(path: Path):
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)


# ── helpers ───────────────────────────────────────────────────────────

_ARCHIVE_SUFFIXES = {".zip", ".tar", ".gz", ".bz2", ".tgz", ".rar"}


def _is_archive(file_path: Path) -> bool:
    """Check if the file looks like an archive by its suffixes."""
    return bool(set(file_path.suffixes) & _ARCHIVE_SUFFIXES)
