# Zipignore

`zipignore` is a lightweight command-line tool for zipping project folders while excluding files and directories using rules defined in a `.zipignore` file. It works similarly to `.gitignore`, making it easy to exclude build artifacts, logs, cache files, or virtual environments from the archive.

---

## Features

- Recursively zips the current directory or a specified folder
- Supports `.zipignore` for exclusion rules
- Generates zip files with timestamped filenames (e.g. `myproject_2025-05-14_18-30-00.zip`)
- Includes a progress bar during the zipping process
- Logs events to a log file and the terminal
- Saves the name of the last generated archive to `.last_zipignore`

---

## Installation

### Option 1: Install from GitHub using `uv`

```bash
uv add git+https://github.com/your-username/zipignore.git
````

### Option 2: Clone and install locally in editable mode

```bash
git clone https://github.com/your-username/zipignore.git
cd zipignore
pip install -e .
```

---

## Usage

Run the tool from the root of your project:

```bash
zipignore
```

By default, it will:

1. Load ignore patterns from `.zipignore`
2. Create a zip file in the current directory
3. Save the zip file name to `.last_zipignore`

---

## Example `.zipignore`

```txt
# Python cache and virtual environment
__pycache__/
*.pyc
.venv/
.env

# Editor config folders
.vscode/
.idea/

# Build output
build/
dist/
*.egg-info/
```

---

## Programmatic Usage

If you prefer to use `zipignore` from a Python script:

```python
from zipignore.core import zip_project

zip_project()
```

---

## Running Tests

To run the unit tests:

```bash
pytest
```

Make sure to activate your virtual environment and install the dev dependencies.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Feel free to open issues or submit pull requests. Suggestions and improvements are always welcome.

---

