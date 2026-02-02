"""Setup configuration for CLI ToDo App."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="cli-todo",
    version="1.0.0",
    description="A minimal command-line application for managing personal tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="CLI Todo Contributors",
    url="https://github.com/gianfranco-omnigpt/cli-todo-5",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="cli todo task-manager terminal productivity",
    entry_points={
        "console_scripts": [
            "todo=todo.__main__:main",
        ],
    },
)
