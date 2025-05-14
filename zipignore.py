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
    # Make all lower case
    filename = filename.lower()
    # Replace symbols for "_" to universal integration
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def get_default_zip_name(base_folder="."):
    logger.debug("Preparing the file name ...")
    folder_name = Path(base_folder).resolve().name
    folder_name = sanitize_filename(folder_name)
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{folder_name}_{date_str}.zip"


IGNORE_FILE = ".zipignore"
ZIP_NAME = get_default_zip_name()

def load_ignore_patterns():
    logger.debug("Loading the patterns to ignore ...")
    patterns = set()

    if Path(IGNORE_FILE).exists():
        with open(IGNORE_FILE, "r") as file:
            for line in file:
                line = line.split("#", 1)[0].strip()
                if line:
                    patterns.add(line)
    return patterns


def should_ignore(path: str, patterns: set) -> bool:
    return any(
        fnmatch(path, pattern) or any(fnmatch(part, pattern) for part in Path(path).parts)
        for pattern in patterns
    )




def zip_project(base_folder="."):
    logger.info("Preparing to zip files ...")
    patterns = load_ignore_patterns()

    # Recolectar todos los archivos primero
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
        for full_path, rel_path in tqdm(file_list, desc="Zipping files", unit="file", ncols=80):
            if not should_ignore(rel_path, patterns):
                zipf.write(full_path, rel_path)
                added += 1

    # Usar tqdm.write para evitar conflictos con la barra
    tqdm.write(f"Zipped {added} files into {ZIP_NAME}")
    logger.success(f"Archive ready: {ZIP_NAME}")

    # Guardar el nombre del zip
    with open(".last_zipignore", "w") as f:
        f.write(ZIP_NAME)




if __name__ == "__main__":
    try:
        zip_project()
    except Exception as e:
        logger.exception("An unexpected error occurred.")
