# Importing dependencies
from pathlib import Path

import pandas as pd
import numpy as np

import fastf1

target_year = 2026 # The year we want to get predictions on
start_year = 2022 # The year from which we should start collecting training data
test_year = target_year - 1

assert start_year <= target_year - 4, "Start at least four years before the target to leave enough training races."

cache = Path('austin_cache')