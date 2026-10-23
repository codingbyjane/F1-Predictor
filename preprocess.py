# Importing dependencies
from pathlib import Path

import pandas as pd
import numpy as np

# FastF1 API for data retrieval
import fastf1

print('FastF1', fastf1.__version__,)

target_year = 2026 # The year we want to get predictions on
start_year = 2022 # The year from which data collection starts
test_year = target_year - 1 # Reserving the previous season for testing the model

assert start_year <= target_year - 4, "Start at least four years before the target to leave enough race data for training."

cache = Path('austin_cache') # Create a Path object representing a folder named "austin_cache"
cache.mkdir(parents=True, exist_ok=True) # Create the cache folder and prevent any errors if the folder already exists

# Enable caching
fastf1.Cache.enable_cache(str(cache))