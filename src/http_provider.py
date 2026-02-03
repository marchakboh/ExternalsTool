import urllib.request
import urllib.error
from pathlib import Path

from base_provider import BaseProvider


class HttpProvider(BaseProvider):
    """
    Downloads assets over plain HTTPS.
    Works with any direct download URL — no special cloud auth required.
    Uses only stdlib (urllib) — no extra dependencies.
    """

    CHUNK_SIZE = 8 * 1024  # 8 KB read chunks

    @property
    def name(self) -> str:
        return "HTTP"

    def download(self, url: str, dest_dir: Path, log_callback) -> Path | None:
        dest_dir.mkdir(parents=True, exist_ok=True)

        # derive filename from URL, fall back to "download" if path is empty
        url_path = url.split("?")[0]                          # strip query params
        filename = url_path.split("/")[-1] or "download"
        dest_file = dest_dir / filename

        log_callback(f"  [HTTP] Downloading: {url}")

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AssetPull/1.0"})
            with urllib.request.urlopen(req) as response:
                total = int(response.headers.get("Content-Length", 0))
                downloaded = 0

                with open(dest_file, "wb") as out:
                    while True:
                        chunk = response.read(self.CHUNK_SIZE)
                        if not chunk:
                            break
                        out.write(chunk)
                        downloaded += len(chunk)

                        if total > 0:
                            pct = int(downloaded / total * 100)
                            log_callback(f"  [HTTP] {pct}% ({downloaded}/{total} bytes)")

            log_callback(f"  [HTTP] Saved: {dest_file}")
            return dest_file

        except urllib.error.HTTPError as e:
            log_callback(f"  [HTTP] ERROR: HTTP {e.code} — {e.reason}")
            return None
        except urllib.error.URLError as e:
            log_callback(f"  [HTTP] ERROR: {e.reason}")
            return None
        except Exception as e:
            log_callback(f"  [HTTP] ERROR: {e}")
            return None
