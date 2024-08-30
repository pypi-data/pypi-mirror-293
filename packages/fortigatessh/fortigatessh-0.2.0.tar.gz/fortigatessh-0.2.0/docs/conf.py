#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2024 Nathan Liang

import os
import sys
from setuptools_scm import get_version

sys.path.insert(0, os.path.abspath("../fortigatessh"))

release = get_version(root="..", relative_to=__file__)

version = release

project = "FortigateSSH"
copyright = "2024, Nathan Liang"
author = "Nathan Liang"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
