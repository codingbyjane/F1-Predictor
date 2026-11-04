# Importing dependencies
from pathlib import Path

import pandas as pd
import numpy as np

import time
from datetime import timezone, datetime

# FastF1 API for data retrieval
import fastf1
from fastf1.ergast import Ergast

print('FastF1', fastf1.__version__,)

target_year = 2026 # The year we want to get predictions on
start_year = 2022 # The year from which data collection starts
test_year = target_year - 1 # Reserving the previous season for testing the model

assert start_year <= target_year - 4, "Start at least four years before the target to leave enough race data for training."

# Access the project's root directory
project_dir = Path(__file__).resolve().parent

cache = project_dir / "austin_cache" # Assign the cache folder to a variable for easy access, specify that the cache folder is located in the project root directory
cache.mkdir(parents=True, exist_ok=True) # Create the cache folder and prevent any errors if the folder already exists

# Enable caching
fastf1.Cache.enable_cache(str(cache)) # Convert the cache object into a fastf1 API string-format

api = Ergast(limit=100) # Create an instance of the Ergast API and set pagination limit to 100 items per page

# Define a retry helper
def retry(function):
    for attempt in range(4): # makes 4 attempts to run the passed function
        
        # Exception handling
        try:
            return function() # returns the result of the supplied function if there are no errors
        
        except Exception: # Use Exception to catch a wide range of possible APIruntime errors  
            if attempt == 3:
                raise # raise the error message after the fourth attempt

            time.sleep(2 ** (attempt + 1)) # pausing the program (exponential backof) for 2, 4, and 8 seconds between consecutive attempts

# Get season results
def season_results(year):
    path = cache / f"results_{year}_{datetime.now(timezone.utc):%Y%m%d}.csv" # Create a path to the cache folder with the filename formatted to include the current date and time with UTC timezone information attached (limit the name to year/month/day)

    if path.exists():
        return pd.read_csv(path, parse_dates=['raceDate'])

    page = retry(lambda: api.get_race_results(season=year)) # 

    chunks = []
    recieved = 0

    while True:
        for (_, meta), result in zip(page.description.iterrows(), page.content):
            results_df = pd.DataFrame(result).copy() # save the race results into a dataframe and make a copy of it to avoid overwriting the original data

            for col_name in ['season', 'round', 'raceName', 'raceDate', 'circuitId']:
                results_df[col_name] = meta[col_name] # add the metadata columns to the results dataframe

            chunks.append(results_df) # append the paginated results dataframe to the chunks list
            recieved += len(results_df) # increment the received counter by the number of rows in the results dataframe