#!/usr/bin/env python3
import json
import zipfile
import logging
import shutil
from pathlib import Path
import build.templates as templates
from utils import REPO_URL, REPO_ROOT, DIST_DIR, PACKS_DIR, is_debug


def get_pack_files(pack_src, pack_name, exclude_dir=None):
    """Yields (source_path, archive_path) for every file in the pack."""
    # Always include the license from repo root
    yield (REPO_ROOT / "LICENSE", Path("LICENSE"))

    for file in pack_src.rglob("*"):
        if not file.is_file():
            continue

        rel_path = file.relative_to(pack_src)
        parts = rel_path.parts

        # Filter: Skip marketing or explicitly excluded dirs (assets/data)
        if "marketing" in parts or (exclude_dir and exclude_dir in parts):
            continue

        # Filter: Handle testing logic
        if "test" in parts:
            if is_debug():
                # Replace "test" folder in path with the pack name
                rel_path = Path(*(pack_name if p == "test" else p for p in parts))
            else:
                continue

        yield (file, rel_path)


def create_zip(out_path, file_generator, extra_files=None):
    """
    Creates zip files based on the generator and handle common filtering/adding logic.
    """
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        if is_debug():
            zf.writestr(
                "DEBUG",
                "This is a debug build and may have extra functionality that won't show up in regular game. Be careful!",
            )

        for src, arc in file_generator:
            zf.write(src, arc)

        if extra_files:
            for name, content in extra_files.items():
                zf.writestr(name, content)


def run_build(pack_name):
    """
    Builds a pack directory into the required .zip files
    """
    pack_src = PACKS_DIR / pack_name
    mcmeta_path = pack_src / "pack.mcmeta"

    if not pack_src.exists() or not mcmeta_path.exists():
        logging.error(f"Missing source or mcmeta for {pack_name}")
        return None

    try:
        with open(mcmeta_path, "r") as f:
            mcmeta_data = json.load(f)
    except json.JSONDecodeError:
        logging.error(f"Failed to parse JSON in {mcmeta_path}")
        return None

    metadata = mcmeta_data.get("metadata", {})
    pack_conf = mcmeta_data.get("pack", {})
    modrinth_conf = metadata.get("modrinth", {})
    version = metadata.get("version", "0.0.1")
    mc_ver = metadata.get("minecraft_version", "1.21.11")

    # Context for templates
    ctx = {
        "id": pack_name,
        "version": version,
        "description": pack_conf.get("description", ""),
        "homepage": f"https://modrinth.com/datapack/{modrinth_conf.get('project_name')}",
        "sources": f"{REPO_URL}/tree/main/packs/{pack_name}",
        "issues": f"{REPO_URL}/issues",
    }

    # Define the Build Plan
    plans = [
        {"suffix": "dp", "exclude": "assets", "mcmeta_patch": metadata.get("dp")},
        {"suffix": "rp", "exclude": "data", "mcmeta_patch": metadata.get("rp")},
        {
            "suffix": "mod",
            "exclude": None,
            "mcmeta_patch": None,
            "virtual_files": {
                "fabric.mod.json": templates.get_fabric_json(ctx),
                "quilt.mod.json": templates.get_quilt_json(ctx),
                "META-INF/mods.toml": templates.get_forge_toml(ctx, "lowcodefml"),
                "META-INF/neoforge.mods.toml": templates.get_forge_toml(ctx, "javafml"),
            },
        },
    ]

    created = []
    for p in plans:
        out_file = (
            DIST_DIR
            / f"{pack_name}-{version}-{mc_ver}-{p['suffix']}.{'jar' if p['suffix'] == 'mod' else 'zip'}"
        )

        # 1. Prepare file stream
        files = get_pack_files(pack_src, pack_name, p["exclude"])

        # 2. Handle dynamic mcmeta overwriting
        extras = p.get("virtual_files", {}).copy()
        if p["mcmeta_patch"]:
            files = ((s, a) for s, a in files if a.name != "pack.mcmeta")
            new_mcmeta = {"pack": {**pack_conf, **p["mcmeta_patch"]}}
            extras["pack.mcmeta"] = json.dumps(new_mcmeta, indent=2)

        create_zip(out_file, files, extras)
        created.append(out_file)
        logging.debug(f"Created {p['suffix']} for {pack_name}")

    logging.info(f"Built {pack_name}: {[f.name for f in created]}")
    return created


def clean_build():
    """
    Cleans and reinitializes the DIST_DIR so that builds can proceed as usual
    """
    # Initialize dist directory
    shutil.rmtree(DIST_DIR, ignore_errors=True)
    DIST_DIR.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    import sys

    # Handle single arg or build all
    target = sys.argv[1] if len(sys.argv) > 1 else None

    clean_build()

    if target:
        run_build(target)
    else:
        for d in PACKS_DIR.iterdir():
            if d.is_dir():
                run_build(d.name)
