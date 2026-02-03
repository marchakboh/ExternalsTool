import json
from dataclasses import dataclass, asdict
from pathlib import Path


# ── data model ────────────────────────────────────────────────────────

@dataclass
class AssetEntry:
    """Single asset record as stored in Database.json."""
    name:     str
    location: str   # relative path inside the project root
    type:     str   # provider name: "Mega", "HTTP", ...
    url:      str   # source URL / link


# ── JSON keys ─────────────────────────────────────────────────────────

_JSON_FILE  = "Database.json"
_JSON_KEY   = "Assets"


# ── public API ────────────────────────────────────────────────────────

def load_config(config_dir: Path) -> list[AssetEntry]:
    """
    Read Database.json from config_dir.
    Returns an empty list if the file doesn't exist yet.
    """
    path = config_dir / _JSON_FILE
    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [AssetEntry(**entry) for entry in data.get(_JSON_KEY, [])]


def save_config(config_dir: Path, entries: list[AssetEntry]) -> None:
    """Write the current asset list to Database.json."""
    config_dir.mkdir(parents=True, exist_ok=True)
    path = config_dir / _JSON_FILE

    data = {_JSON_KEY: [asdict(e) for e in entries]}

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
