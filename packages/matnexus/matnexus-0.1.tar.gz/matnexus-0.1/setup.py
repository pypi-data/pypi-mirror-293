#!/usr/bin/env python3
"""
Setup script for MatNexus
© Lei Zhang, Markus Stricker, 2023
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name="MatNexus",
    version="0.1",
    description="Library for natural language processing for scientific papers",
    long_description=open(path.join(here, "README.md")).read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.ruhr-uni-bochum.de/icams-mids/text_mining_tools",
    author="Lei Zhang",
    author_email="Lei.Zhang-w2i@ruhr-uni-bochum.de",
    license="GNU GPL v3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="physics, energy, material science, natural language processing",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "colorama",
        "matplotlib",
        "charset-normalizer",
        "plotly",
        "numpy",
        "seaborn",
        "spacy>=3.0.0",
        "nltk",
        "certifi",
        "requests",
        "pandas",
        "idna",
        "packaging",
        "scikit-learn",
        "gensim",
        "black",
        "notebook",
        "flake8",
        "pybliometrics",
    ],
    python_requires='>=3.10',
)