from setuptools import setup, find_packages

setup(
    name="study-timer-pro",
    version="1.0.0",
    description="A feature-rich Pomodoro timer with analytics and distraction blocking",
    author="Rishabh Rai",
    author_email="rairishabh280@gmail.com",
    url="https://github.com/RishabhRai280/study-timer-pro",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "pygame",
        "matplotlib",
        "numpy",
        "Pillow",
        "psutil",
        "plyer",
        "requests",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "study-timer-pro=src.main:main",
        ],
    },
)
