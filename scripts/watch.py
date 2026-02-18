#!/usr/bin/env python3

import time
import logging
from datetime import datetime
from utils import PACKS_DIR
from build import run_build, clean_build
from install import run_install


def get_pack_from_path(file_path):
    """
    Determines which pack a file belongs to by looking at its parent
    directories relative to the /packs folder.
    """
    try:
        # Get the relative path from the packs directory
        # e.g., 'headless_tools/data/...' -> 'headless_tools'
        relative = file_path.relative_to(PACKS_DIR)
        return relative.parts[0] if relative.parts else None
    except ValueError:
        return None


def watch():
    logging.info("Rebuilding all packs")
    clean_build()
    for d in PACKS_DIR.iterdir():
        if d.is_dir():
            build_files = run_build(d.name)
            run_install(build_files)

    logging.info("Monitoring /packs for changes...")

    # Initial snapshot of file modification times
    snapshot = {p: p.stat().st_mtime for p in PACKS_DIR.rglob("*") if p.is_file()}

    try:
        while True:
            time.sleep(2)
            current = {
                p: p.stat().st_mtime for p in PACKS_DIR.rglob("*") if p.is_file()
            }

            # Detect changes (new, modified, or deleted files)
            if current != snapshot:
                # Identify which packs need a rebuild
                changed_packs = set()

                # Check for modified or new files
                for path, mtime in current.items():
                    if path not in snapshot or mtime != snapshot[path]:
                        pack_name = get_pack_from_path(path)
                        if pack_name:
                            changed_packs.add(pack_name)

                # Check for deleted files
                for path in snapshot:
                    if path not in current:
                        pack_name = get_pack_from_path(path)
                        if pack_name:
                            changed_packs.add(pack_name)

                # Only rebuild the packs that actually changed
                for pack_name in changed_packs:
                    logging.info(f"Change detected in [{pack_name}]! Rebuilding...")
                    build_files = run_build(pack_name)
                    run_install(build_files)

                logging.info(f"Rebuilt at {datetime.now()}\n")
                snapshot = current

    except KeyboardInterrupt:
        logging.info("Watcher stopped.")


if __name__ == "__main__":
    watch()
