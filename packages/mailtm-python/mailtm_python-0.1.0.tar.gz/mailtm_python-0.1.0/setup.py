# setup.py

import os
import re
from setuptools import setup, find_packages

# Function to dynamically get the version from __init__.py
def get_version():
    init_path = os.path.join(os.path.dirname(__file__), 'mailtm', '__init__.py')
    with open(init_path, 'r') as f:
        content = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# Function to read the README.md file for the long description
def read_long_description():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_path, 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name="mailtm-python",
    version=get_version(),  # Dynamically get the version
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    description="A Python SDK for interacting with the Mail.tm API",
    long_description=read_long_description(),  # Add long description from README.md
    long_description_content_type="text/markdown",  # Specify the format of the long description
    author="Adnan Ahmad",
    author_email="viperadnan@gmail.com",
    url="https://github.com/viperadnan-git/mailtm-python-sdk",
    license="GPLv3",  # Specify the GPLv3 license
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
