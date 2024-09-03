import setuptools
from pathlib import Path

try:
    readme_path = Path("README.md")

    setuptools.setup(
        name="wurapdf",
        version="1.0",
        long_description=readme_path.read_text(),
        packages=setuptools.find_packages(exclude=['test', 'data'])
    )

except FileNotFoundError:
    print("File not found")
