"""
AssetPull — config-driven asset sync for game projects.

Usage:
    # GUI mode
    python main.py --app --root_folder <PROJECT_ROOT> --config_folder <CONFIG_PATH>

    # CLI mode (syncs everything in the config, no prompts)
    python main.py --root_folder <PROJECT_ROOT> --config_folder <CONFIG_PATH>
"""

import argparse
from pathlib import Path

from config import load_config
from sync_runner import SyncRunner


def main():
    parser = argparse.ArgumentParser(
        description="AssetPull — asset sync for game projects"
    )
    parser.add_argument("--app",           action="store_true", help="Launch GUI")
    parser.add_argument("--root_folder",   required=True,       help="Project root directory")
    parser.add_argument("--config_folder", required=True,       help="Config directory (Database.json lives here)")

    args = parser.parse_args()

    root_dir   = Path(args.root_folder).resolve()
    config_dir = Path(args.config_folder).resolve()
    temp_dir   = config_dir / "Temp"

    if args.app:
        # ── GUI mode ──────────────────────────────────────────────
        from main_window import MainWindow
        MainWindow.show_window(root_dir, config_dir)
    else:
        # ── CLI mode — sync everything ────────────────────────────
        entries = load_config(config_dir)
        if not entries:
            print("No assets in config. Nothing to do.")
            return

        runner = SyncRunner(root_dir, temp_dir, log_callback=print)
        runner.run(entries)


if __name__ == "__main__":
    main()
