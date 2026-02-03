from abc import ABC, abstractmethod
from pathlib import Path


class BaseProvider(ABC):
    """
    Abstract base for all download providers.
    Each provider knows how to fetch a single asset from its source.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable provider name, e.g. 'Mega', 'HTTP'."""
        ...

    @abstractmethod
    def download(self, url: str, dest_dir: Path, log_callback) -> Path | None:
        """
        Download the file at `url` into `dest_dir`.

        Args:
            url:          Source URL / link for this provider.
            dest_dir:     Directory where the downloaded file should land.
            log_callback: Callable(str) — provider pushes progress lines here.

        Returns:
            Path to the downloaded file, or None on failure.
        """
        ...
