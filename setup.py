#!/usr/bin/env python3
"""
Setup script for Study Timer Pro
"""

from setuptools import setup, find_packages

setup(
    name="study-timer-pro",
    version="2.1.0",
    description="A comprehensive Pomodoro timer application with productivity features",
    author="Study Timer Pro Team",
    author_email="contact@studytimerpro.com",
    url="https://github.com/RishabhRai280/study-timer-pro",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "pygame>=2.5.0",
        "matplotlib>=3.7.0",
        "numpy>=1.24.0",
        "Pillow>=10.0.0",
        "psutil>=5.9.0",
        "plyer>=2.1.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "study-timer-pro=main:main",
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
)