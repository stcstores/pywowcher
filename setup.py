#!/usr/bin/env python
"""Setup for pywowcher package."""

import os

import setuptools

with open("README.rst", "r") as readme:
    long_description = readme.read()

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, "pywowcher", "__version__.py"), "r") as f:
    exec(f.read(), about)

setuptools.setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    keywords=["Wowcher", "api", "shopping"],
    install_requires=["requests", "pyaml"],
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.5.0",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Utilities",
        "Topic :: Other/Nonlisted Topic",
    ],
)
