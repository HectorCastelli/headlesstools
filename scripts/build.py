#!/usr/bin/env python3

import json
import zipfile
import logging
import shutil
from utils import PREFIX, REPO_ROOT, DIST_DIR, PACKS_DIR


def run_build(pack_name):
    pack_src = PACKS_DIR / pack_name
    mcmeta_file = PACKS_DIR / pack_name / "pack.mcmeta"
    if not pack_src.exists():
        logging.error(f"Source folder not found: {pack_src}")
        return None
    if not mcmeta_file.exists():
        logging.error(f"Source folder does not have a pack.mcmeta file: {pack_src}")
        return None

    try:
        with open(mcmeta_file, "r") as f:
            mcmeta_data = json.load(f)
            logging.debug(f"Read mcmeta for {pack_name}")
    except json.JSONDecodeError:
        logging.error(f"Failed to parse JSON in {mcmeta_file}")
        return None

    pack_data = mcmeta_data.get("pack", {})
    metadata = mcmeta_data.get("metadata", {})
    version = metadata.get("version")
    minecraft_version = metadata.get("minecraft_version", "1.21.11")
    dp_meta = metadata.get("dp")
    rp_meta = metadata.get("rp")
    if version is None:
        logging.error(f"Pack {pack_name} has no 'version' defined in 'metadata'")
        return None

    created_files = []

    # Build packs
    for suffix, exclude_dir, extra_mcmeta in [
        ("dp", "assets", dp_meta),
        ("rp", "data", rp_meta),
    ]:
        out_file = (
            DIST_DIR
            / f"{PREFIX}-{pack_name}-{minecraft_version}-{version}-{suffix}.zip"
        )
        with zipfile.ZipFile(out_file, "w", zipfile.ZIP_DEFLATED) as zf:
            # Copy global files (e.g., LICENSE)
            zf.write(REPO_ROOT / "LICENSE", "LICENSE")

            # Copy pack files with exclusions
            for file in pack_src.rglob("*"):
                if file.is_file():
                    rel_path = file.relative_to(pack_src)

                    # Skip original mcmeta if it should be rewritten
                    if extra_mcmeta and rel_path.name == "pack.mcmeta":
                        continue

                    # If the directory was explicitly excluded
                    if exclude_dir in rel_path.parts:
                        continue

                    zf.write(file, rel_path)

            # Generate a pack.mcmeta if needed
            if extra_mcmeta:
                final_mcmeta = {"pack": {**pack_data, **extra_mcmeta}}
                zf.writestr("pack.mcmeta", json.dumps(final_mcmeta, indent=2))

        created_files.append(out_file)
        logging.debug(f"Created {suffix}pack for {pack_name}")

    logging.info(f"Built {pack_name}: {' '.join([f.name for f in created_files])}")
    return created_files


def clean_build():
    # Initialize dist directory
    shutil.rmtree(DIST_DIR, ignore_errors=True)
    DIST_DIR.mkdir(exist_ok=True)


if __name__ == "__main__":
    import sys

    # Handle single arg or build all
    target = sys.argv[1] if len(sys.argv) > 1 else None

    clean_build

    if target:
        run_build(target)
    else:
        for d in PACKS_DIR.iterdir():
            if d.is_dir():
                run_build(d.name)
