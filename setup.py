import pathlib

from setuptools import setup, find_packages

try:
    long_description = (pathlib.Path(__file__).parent / "README.md").read_text()
except:
    long_description = None
setup(
    name="graphs",
    version="0.0.2",
    author="rshanker779",
    author_email="rshanker779@gmail.com",
    description="Graph theory in Python",
    long_description=long_description
    if long_description is not None
    else "Graph theory in Python",
    license="MIT",
    python_requires=">=3.7",
    install_requires=[
        "rshanker779_common~=0.0",
        "matplotlib~=3.2",
        "numpy~=1.18",
        "more_itertools~=8.2",
        "pytest_cases~=1.13",
    ],
    packages=find_packages(),
    entry_points={},
)
