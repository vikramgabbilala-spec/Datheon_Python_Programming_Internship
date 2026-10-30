#!/usr/bin/env python3
"""Organize files into extension-based folders without overwriting existing files."""

import argparse
import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Iterator


EXTENSION_CATEGORIES = {
    ".doc": "Documents",
    ".docx": "Documents",
    ".odt": "Documents",
    ".pdf": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".rtf": "Documents",
    ".txt": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",
    ".csv": "Documents",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".bmp": "Images",
    ".tif": "Images",
    ".tiff": "Images",
    ".webp": "Images",
    ".svg": "Images",
    ".heic": "Images",
    ".mp4": "Videos",
    ".m4v": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",
    ".mkv": "Videos",
    ".webm": "Videos",
    ".wmv": "Videos",
    ".mp3": "Audio",
    ".wav": "Audio",
    ".flac": "Audio",
    ".aac": "Audio",
    ".ogg": "Audio",
    ".m4a": "Audio",
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
    ".bz2": "Archives",
    ".xz": "Archives",
    ".py": "Code",
    ".js": "Code",
    ".ts": "Code",
    ".jsx": "Code",
    ".tsx": "Code",
    ".html": "Code",
    ".css": "Code",
    ".java": "Code",
    ".c": "Code",
    ".h": "Code",
    ".cpp": "Code",
    ".hpp": "Code",
    ".cs": "Code",
    ".go": "Code",
    ".rs": "Code",
    ".php": "Code",
    ".rb": "Code",
    ".sh": "Code",
    ".sql": "Code",
    ".json": "Code",
    ".yaml": "Code",
    ".yml": "Code",
    ".xml": "Code",
}


def iter_files(root: Path, recursive: bool, logger: logging.Logger) -> Iterator[Path]:
    """Yield regular files, never following symlinks or revisiting output folders."""
    try:
        with os.scandir(root) as entries:
            for entry in entries:
                path = Path(entry.path)
                try:
                    if entry.is_symlink():
                        continue
                    if entry.is_file(follow_symlinks=False):
                        yield path
                    elif recursive and entry.is_dir(follow_symlinks=False):
                        if path.parent == root and entry.name in {
                            *EXTENSION_CATEGORIES.values(),
                            "Others",
                            "Audio",
                        }:
                            continue
                        yield from iter_files(path, recursive, logger)
                except OSError as error:
                    logger.warning("Skipped %s: %s", path, error)
    except OSError as error:
        logger.warning("Could not scan %s: %s", root, error)


def destination_for(source: Path, root: Path) -> Path:
    category = EXTENSION_CATEGORIES.get(source.suffix.lower(), "Others")
    destination_dir = root / category
    destination = destination_dir / source.name
    if not destination.exists():
        return destination

    stem, suffix = source.stem, source.suffix
    index = 1
    while True:
        candidate = destination_dir / "{} ({}){}".format(stem, index, suffix)
        if not candidate.exists():
            return candidate
        index += 1


def organize(root: Path, recursive: bool, dry_run: bool, logger: logging.Logger) -> tuple:
    moved = skipped = failed = 0
    files = list(iter_files(root, recursive, logger))

    for source in files:
        try:
            destination = destination_for(source, root)
            if dry_run:
                logger.info("Would move %s -> %s", source, destination)
                moved += 1
                continue

            destination.parent.mkdir(exist_ok=True)
            shutil.move(str(source), str(destination))
            logger.info("Moved %s -> %s", source, destination)
            moved += 1
        except PermissionError as error:
            logger.warning("Permission denied; skipped %s: %s", source, error)
            skipped += 1
        except OSError as error:
            logger.error("Could not move %s: %s", source, error)
            failed += 1

    return moved, skipped, failed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sort files into Documents, Images, Videos, Audio, Archives, Code, and Others."
    )
    parser.add_argument("directory", type=Path, help="directory whose files should be organized")
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="also organize files in nested directories (outputs remain in the selected directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show planned moves without creating folders or moving files",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logger = logging.getLogger("organizer")
    root = args.directory.expanduser().resolve()
    if not root.is_dir():
        parser.error("directory does not exist or is not a directory: {}".format(root))

    moved, skipped, failed = organize(root, args.recursive, args.dry_run, logger)
    logger.info(
        "Summary: %d %s, %d skipped, %d failed",
        moved,
        "planned" if args.dry_run else "moved",
        skipped,
        failed,
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
