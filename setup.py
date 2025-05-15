from setuptools import setup, find_packages

setup(
    name="zipignore",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "loguru",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "zipignore=zipignore.cli:main"
        ]
    },
)
