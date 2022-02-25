#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="{{cookiecutter.project_name}}",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "{{cookiecutter.project_name}} = {{cookiecutter.project_slug}}.main:main",
        ]
    },
)
