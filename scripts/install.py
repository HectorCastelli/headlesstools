#!/usr/bin/env python3
import os
import shutil
import logging
from pathlib import Path
from utils import DIST_DIR


def run_install(build_files):
    """
    Takes a list of Path objects (ZIP files) and deploys them to the appropriate Minecraft instance folders based on their filename suffixes.
    """
    if not build_files:
        logging.warning("No build files provided for installation.")
        return

    instance_path = os.getenv("INSTANCE_PATH")
    WORLD_NAME = os.getenv("WORLD_NAME", "New World")  # Default to standard name

    if not instance_path:
        logging.error("INSTANCE_PATH not defined in .env. Skipping installation.")
        return

    # Define standard Minecraft destination paths
    datapack_dir = Path(instance_path) / "saves" / WORLD_NAME / "datapacks"
    resource_dir = Path(instance_path) / "resourcepacks"

    try:
        # Ensure destination directories exist
        datapack_dir.mkdir(parents=True, exist_ok=True)
        resource_dir.mkdir(parents=True, exist_ok=True)

        for file_path in build_files:
            filename = file_path.name

            # Determine destination based on the file suffix logic from build.py
            if filename.lower().endswith("-dp.zip"):
                dest = datapack_dir / filename
                shutil.copy2(file_path, dest)
                logging.info(f"Installed Datapack: {filename}")

            elif filename.lower().endswith("-rp.zip"):
                dest = resource_dir / filename
                shutil.copy2(file_path, dest)
                logging.info(f"Installed Resourcepack: {filename}")

            else:
                # Copy to both as a fallback.
                shutil.copy2(file_path, datapack_dir / filename)
                shutil.copy2(file_path, resource_dir / filename)
                logging.warning(
                    f"Installed unrecognized pack: {filename} (to both folders)"
                )

    except Exception as e:
        logging.error(f"Failed to install files: {e}")
        return None

    return True


if __name__ == "__main__":
    for d in DIST_DIR.iterdir():
        if d.is_file():
            run_install([d])

    logging.info("Installation process complete.")
