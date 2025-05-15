from zipignore.logger import setup_loguru, logger
setup_loguru("DEBUG")

import zipfile
import os
from pathlib import Path
from fnmatch import fnmatch
from datetime import datetime
import re
from tqdm import tqdm


def sanitize_filename(filename: str) -> str:
    logger.debug("Sanitizing and converting to lower case ...")
    # make all characters lowercase
    filename = filename.lower()
    filename = filename.replace(" ", "_")
    # replace invalid symbols whit "_" for cross-platform compatibility
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def get_default_zip_name(base_folder="."):
    # generate a sanitized and timestamped zip filename based on the current folder name
    logger.debug("Preparing the file name ...")

    normalized_path = Path(base_folder.replace("\\", "/")).resolve()
    folder_name = sanitize_filename(normalized_path.name)

    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{folder_name}_{date_str}.zip"


IGNORE_FILE = ".zipignore"


def load_ignore_patterns():
    # load ignore patterns from .zipignore, removing inline and full-line comments
    logger.debug("Loading the patterns to ignore ...")
    patterns = set()
    # loads all lines in file splitting comments starting with # or containing # next-to
    if Path(IGNORE_FILE).exists():
        with open(IGNORE_FILE, "r") as file:
            for line in file:
                line = line.split("#", 1)[0].strip()
                if line:
                    patterns.add(line)
    return patterns


def should_ignore(path: str, patterns: set) -> bool:
    # split the relative path into parts for granular pattern matching
    path_parts = Path(path).parts
    # check if ignore or not based on the loaded patterns from .zipignore
    for pattern in patterns:
        # check if the full path matches any ignore pattern
        if fnmatch(path, pattern):
            return True
        # check if any part of the path matches a pattern (e.g., subfolders or files)
        if any(fnmatch(part, pattern) for part in path_parts):
            return True
        # check if the path starts with an ignored directory pattern
        if pattern.endswith("/") and str(Path(path)).startswith(pattern.rstrip("/")):
            return True
    return False




def zip_project(base_folder=".", zip_name=None, dry_run=False):
    logger.info("Preparing to zip files ...")

    if zip_name is None:
        zip_name = get_default_zip_name(base_folder)

    patterns = load_ignore_patterns()

    file_list = []
    for root, _, files in os.walk(base_folder):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, base_folder)
            file_list.append((full_path, rel_path))

    total_files = len(file_list)
    if total_files == 0:
        logger.warning("No files found to zip.")
        return

    added = 0
    tqdm.write(f"Total files to check before filtering: {total_files}")

    if dry_run:
        tqdm.write("Dry run mode: these files would be included:")
        for _, rel_path in file_list:
            if not should_ignore(rel_path, patterns):
                print(rel_path)
        return

    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for full_path, rel_path in tqdm(file_list, desc="Zipping files", unit="file", ncols=80):
            if not should_ignore(rel_path, patterns):
                zipf.write(full_path, rel_path)
                added += 1

    tqdm.write(f"Zipped {added} files into {zip_name}")
    logger.success(f"Archive ready: {zip_name}")

    with open(".last_zipignore", "w") as f:
        f.write(zip_name)





