from setuptools import setup, find_packages
import os

try:
    with open(os.path.join(os.path.dirname(__file__)), "README.md") as f:
        long_description = f.read()
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
    test_suite="graphs/tests",
)
