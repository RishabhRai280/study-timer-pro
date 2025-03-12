#!/usr/bin/env python3
"""
Setup script for Study Timer Pro
"""

from setuptools import setup, find_packages
import pathlib

# Read long description from README.md
HERE = pathlib.Path(__file__).parent
long_description = (HERE / "README.md").read_text()

# Read dependencies from requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="study-timer-pro",
    version="2.1.0",
    description="A comprehensive Pomodoro timer application with productivity features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Study Timer Pro Team",
    author_email="rairishabh280@gmail.com",
    url="https://github.com/RishabhRai280/study-timer-pro",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=requirements,  # Dynamically loads dependencies
    entry_points={
        "console_scripts": [
            "study-timer-pro=src.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    license="MIT",
)
