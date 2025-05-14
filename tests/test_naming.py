from zipignore import get_default_zip_name, sanitize_filename
import re

def test_sanitize_filename():
    assert sanitize_filename("Hello:World*Test?.zip") == "hello_world_test_.zip"

def test_get_default_zip_name_format():
    name = get_default_zip_name("sample")
    assert re.match(r"sample_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}.zip", name)
