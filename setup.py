from setuptools import setup

setup(
    name="ayrsharehelper",
    version="0.1.0",
    py_modules=["ayrsharehelper"],
    packages=["ayrsharehelper"],
    install_requires=["requests", "click"],
    entry_points={
        "console_scripts": [
            "ash=ayrsharehelper.cli:cli",
        ],
    },
)
