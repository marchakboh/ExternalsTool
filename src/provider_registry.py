from mega_provider import MegaProvider
from http_provider import HttpProvider
from base_provider import BaseProvider

# ── registry ──────────────────────────────────────────────────────────
# Maps the "Type" string from Database.json to a provider class.
# To add a new backend: import it, add one line here. Done.

_REGISTRY: dict[str, type[BaseProvider]] = {
    "Mega": MegaProvider,
    "HTTP": HttpProvider,
}


def get_provider(type_name: str) -> BaseProvider | None:
    """
    Instantiate a provider by its config name.
    Returns None if the type is unknown (logged upstream).
    """
    cls = _REGISTRY.get(type_name)
    if cls is None:
        return None
    return cls()


def available_types() -> list[str]:
    """All registered provider names — used to populate the GUI dropdown."""
    return list(_REGISTRY.keys())
