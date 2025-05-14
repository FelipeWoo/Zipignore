from logger import setup_loguru, logger
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
    # replace invalid symbols whit "_" for cross-platform compatibility
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def get_default_zip_name(base_folder="."):
    # generate a sanitized and timestamped zip filename based on the current folder name
    logger.debug("Preparing the file name ...")
    folder_name = Path(base_folder).resolve().name
    folder_name = sanitize_filename(folder_name)
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{folder_name}_{date_str}.zip"


IGNORE_FILE = ".zipignore"
ZIP_NAME = get_default_zip_name()

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




def zip_project(base_folder="."):
    
    logger.info("Preparing to zip files ...")
    patterns = load_ignore_patterns()

    # collect all files in base_folder recursively (before filtering)
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

    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zipf:
        # create a tqdm progress bar for all scanned files
        for full_path, rel_path in tqdm(file_list, desc="Zipping files", unit="file", ncols=80):
            # filter out files based on ignore patterns
            if not should_ignore(rel_path, patterns):
                zipf.write(full_path, rel_path)
                added += 1

    # log a summary and save the name of the generated zip for further use
    tqdm.write(f"Zipped {added} files into {ZIP_NAME}")
    logger.success(f"Archive ready: {ZIP_NAME}")

    # save the name of the last generated zip archive to a hidden file
    with open(".last_zipignore", "w") as f:
        f.write(ZIP_NAME)




if __name__ == "__main__":
    # Run the zipping process and catch unexpected errors with traceback
    try:
        zip_project()
    except Exception as e:
        logger.exception("An unexpected error occurred.")
