from zipignore import should_ignore

def test_should_ignore_basic_patterns():
    patterns = {"__pycache__/", "*.log", ".env"}
    assert should_ignore("__pycache__/file.pyc", patterns)
    assert should_ignore("debug.log", patterns)
    assert should_ignore(".env", patterns)
    assert not should_ignore("main.py", patterns)