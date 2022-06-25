# pylint: skip-file

import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))

on_rtd = os.environ.get("READTHEDOCS") == "True"
project = "gocomics.py"
copyright = "2022, Omkaar"
author = "Mr.Brawler"
release = "1.1.3"

extensions = ["sphinx.ext.autodoc"]
