#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "CLI tool for accessing Equasis maritime data"

setup(
    name="equasis-cli",
    version="1.0.0",
    author="rhinonix",
    author_email="rhinonix.github.exclaim769@slmail.me",
    description="Command-line tool for accessing Equasis maritime data",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/rhinonix/equasis-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "equasis=equasis_cli.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
