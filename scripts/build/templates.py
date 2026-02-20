import json


def get_fabric_json(ctx):
    return json.dumps(
        {
            "schemaVersion": 1,
            "id": ctx["id"],
            "version": ctx["version"],
            "name": ctx["id"],
            "description": ctx["description"],
            "authors": ["HectorCastelli"],
            "contact": {
                "homepage": ctx["homepage"],
                "sources": ctx["sources"],
                "issues": ctx["issues"],
            },
            "license": "Unlicense",
            "icon": "pack.png",
            "environment": "*",
            "depends": {"fabric-resource-loader-v0": "*"},
        },
        indent=2,
    )


def get_quilt_json(ctx):
    return json.dumps(
        {
            "schema_version": 1,
            "quilt_loader": {
                "group": "io.github.hectorcastelli",
                "id": ctx["id"],
                "version": ctx["version"],
                "metadata": {
                    "name": ctx["id"],
                    "description": ctx["description"],
                    "contributors": {"HectorCastelli": "Member"},
                    "contact": {
                        "homepage": ctx["homepage"],
                        "sources": ctx["sources"],
                        "issues": ctx["issues"],
                    },
                    "icon": "pack.png",
                },
                "intermediate_mappings": "net.fabricmc:intermediary",
                "depends": [
                    {
                        "id": "quilt_resource_loader",
                        "versions": "*",
                        "unless": "fabric-resource-loader-v0",
                    }
                ],
            },
        },
        indent=2,
    )


def get_forge_toml(ctx, loader="lowcodefml"):
    # loader: "lowcodefml" for Forge, "javafml" for NeoForge
    loader_version = "[40,)" if loader == "lowcodefml" else "[1,)"
    return f"""modLoader = "{loader}"
loaderVersion = "{loader_version}"
license = "Unlicense"
showAsResourcePack = false
issueTrackerURL = "{ctx["issues"]}"

[[mods]]
modId = "{ctx["id"]}"
version = "{ctx["version"]}"
displayName = "{ctx["id"]}"
description = "{ctx["description"]}"
logoFile = "pack.png"
updateJSONURL = "https://api.modrinth.com/updates/oJ1q5vHh/forge_updates.json"
authors = "HectorCastelli"
displayURL = "{ctx["homepage"]}"
"""
