# Pranav Minasandra
# 19 May 2026
# pminasandra.github.io

from pathlib import Path

import pandas as pd

import config
import utilities

if not config.SUPPRESS_INFORMATIVE_PRINT:
    old_print = print
    print = utilities.sprint


