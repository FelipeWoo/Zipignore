import zipfile
from zipignore import zip_project, get_default_zip_name
import os

def test_zip_creation(tmp_path):
    # Setup fake project
    project = tmp_path / "project"
    project.mkdir()
    (project / "main.py").write_text("print('hello')")
    (project / "debug.log").write_text("error")
    (project / "__pycache__").mkdir()
    (project / "__pycache__" / "temp.pyc").write_text("")

    # Create .zipignore
    (project / ".zipignore").write_text("__pycache__/")

    os.chdir(project)
    zip_project(".")

    zip_name = [f for f in os.listdir() if f.endswith(".zip")][0]
    with zipfile.ZipFile(zip_name, "r") as z:
        file_list = z.namelist()
        assert "main.py" in file_list
        assert "debug.log" in file_list
        assert "__pycache__/temp.pyc" not in file_list
