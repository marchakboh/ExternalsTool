# AssetPull

A config-driven asset sync utility for projects. Downloads external content from cloud storage and unpacks it into the project — as a lightweight alternative to Git LFS, SVN, or Perforce when you don't need an expensive dedicated server.

Works in two modes: **GUI** (pick what to sync) or **CLI** (sync everything, no prompts). Current backend: [Mega](https://mega.nz/).

Built with **Qt (C++)** and **Python**.

---

## How it works

```
Database.json (config)
        ↓
  AssetPull.exe
  ├── GUI mode (--app)   →  user picks assets via checkboxes
  └── CLI mode           →  syncs all assets automatically
        ↓
  download archive from Mega
        ↓
  extract → project root (or custom path)
```

A `Database.json` configuration file stores info about each registered asset. Both the GUI and CLI versions read from this file. **Commit it to the repository** so the config stays in sync across the team.

---

## Integration

The tool ships as a single `AssetPull.exe` in the `dist` directory. Two ways to bring it into your project:

**Option A — download and drop in:**

Download the repo as an archive, extract `AssetPull.exe` into your project.

**Option B — git submodule:**

```bash
git submodule add https://github.com/marchakboh/AssetPull <DESTINATION>
```

---

## Usage

### Launch parameters

```powershell
AssetPull.exe --app --root_folder <ROOT_PATH> --config_folder <CONFIG_PATH>
```

| Parameter | Required | Description |
|---|---|---|
| `--app` | No | Launches the GUI. Without this flag, runs in console-only mode. |
| `--root_folder` | Yes | Root folder of the target project repository. |
| `--config_folder` | Yes | Folder where `Database.json` config is stored. |

### Recommended setup

Create two `.bat` files in the project root — one for GUI, one for CLI:

**`sync_gui.bat`**
```powershell
@echo off
cd %~dp0Tools\AssetPull\dist
AssetPull.exe --app --root_folder %~dp0 --config_folder %~dp0Tools\AssetPull_config
```

**`sync.bat`**
```powershell
@echo off
cd %~dp0Tools\AssetPull\dist
AssetPull.exe --root_folder %~dp0 --config_folder %~dp0Tools\AssetPull_config
pause
```

---

## Tech

| Layer | Technology |
|---|---|
| GUI | Qt (C++) |
| Cloud sync | Python + megatools (Mega API) |
| Config | `Database.json` |
| Distribution | Single `.exe` + `.bat` wrappers |
