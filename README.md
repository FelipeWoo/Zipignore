# Zipignore

A simple utility to create `.zip` archives while ignoring files and folders defined in a `.zipignore` file — just like `.gitignore` but for zipped projects.

## ✨ Features

- Ignore files/folders using patterns.
- Easily customizable with a `.zipignore` file.
- Portable and dependency-free (pure Python).
- Works great with automation tools like `make`.

## 🚀 Usage

1. Add a `.zipignore` file in your project root:

```txt
# .zipignore example
__pycache__/
*.log
.env
node_modules/
.vscode/
````

2. Run the script:

```bash
python zipignore.py
```

3. The zipped project will be saved as:

```bash
./project_clean.zip
```
