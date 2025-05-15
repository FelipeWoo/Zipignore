from zipignore.core import get_default_zip_name, sanitize_filename
import re
import pytest

def test_sanitize_filename():
    assert sanitize_filename("Hello:World*Test?.zip") == "hello_world_test_.zip"

def test_sanitize_filename_spaces():
    assert sanitize_filename("Hel lo:Wor ld*Tes t?.zip") == "hel_lo_wor_ld_tes_t_.zip"

def test_get_default_zip_name_format():
    # input path and output the full file name
    name = get_default_zip_name("sample") # more paths
    assert re.match(r"sample_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}.zip", name)


@pytest.mark.parametrize("input_path,expected_prefix", [
    (r"C:\Users\Zenon\Documents\My Project", "my_project_"),  
    (r"C:\Test\Weird:Name*Here?", "weird_name_here__"),       
    (r"Some/Unix/Style/Path", "path_"),
])
def test_get_default_zip_name_with_backslashes(input_path, expected_prefix):
    name = get_default_zip_name(input_path)
    pattern = rf"^{re.escape(expected_prefix)}\d{{4}}-\d{{2}}-\d{{2}}_\d{{2}}-\d{{2}}-\d{{2}}\.zip$"
    assert re.match(pattern, name), f"Name '{name}' does not match expected pattern for input '{input_path}'"
