from setuptools import setup, find_packages

setup(
    name="markdown-reformatter",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["replace"],
    entry_points={
        "console_scripts": [
            "replace=replace:main",
        ],
    },
    install_requires=[],
)
