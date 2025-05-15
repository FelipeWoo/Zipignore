import zipfile
import os
from pathlib import Path
from zipignore import zip_project, get_default_zip_name

def test_zip_creation(tmp_path):
    # 🧪 Create fake project directory inside tmp_path
    project = tmp_path / "project"
    project.mkdir()

    # Create files and folders inside the fake project
    (project / "main.py").write_text("print('hello')")
    (project / "debug.log").write_text("error")
    (project / "__pycache__").mkdir()
    (project / "__pycache__" / "temp.pyc").write_text("")

    # Create a .zipignore file that excludes __pycache__/
    (project / ".zipignore").write_text("__pycache__/")

    # 🔁 Save original working directory
    original_cwd = os.getcwd()
    try:
        #  Change working directory to the project
        os.chdir(project)

        #  Generate expected zip file name based on folder name and timestamp
        expected_zip_name = get_default_zip_name(".")

        #  Execute zip logic
        zip_project(".")

        #  Check if the .zip file was actually created
        assert Path(expected_zip_name).is_file(), f"{expected_zip_name} was not created"

        #  Validate contents inside the zip
        with zipfile.ZipFile(expected_zip_name, "r") as z:
            file_list = z.namelist()
            assert "main.py" in file_list
            assert "debug.log" in file_list
            assert "__pycache__/temp.pyc" not in file_list
            assert not any(f.startswith("__pycache__/") for f in file_list)

        #  Validate that .last_zipignore contains the correct file name
        with open(".last_zipignore") as f:
            recorded_name = f.read().strip()
            assert recorded_name == expected_zip_name

    finally:
        #  Restore original working directory to avoid affecting other tests
        os.chdir(original_cwd)
