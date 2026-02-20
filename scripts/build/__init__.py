from .templates import get_fabric_json, get_forge_toml, get_quilt_json

# Re-export to other scripts
__all__ = [
    get_quilt_json,
    get_fabric_json,
    get_forge_toml,
]
