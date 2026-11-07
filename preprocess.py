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
        
        except Exception: # use Exception to catch a wide range of possible API runtime errors  
            if attempt == 3:
                raise # raise the error message after the fourth attempt

            time.sleep(2 ** (attempt + 1)) # pausing the program (exponential backoff) for 2, 4, and 8 seconds between consecutive attempts


# Define a funciton to retrieve season results from the Ergast API and cache them as a CSV file (takes a year argument for the season)
def season_results(year):
    path = cache / f"results_{year}_{datetime.now(timezone.utc):%Y%m%d}.csv" # Create a path to the CSV cache folder with the filename formatted to include the current date and time in UTC (limit the name to year/month/day)

    if path.exists():
        return pd.read_csv(path, parse_dates=['raceDate']) # Read the existing CSV file and return it as a pandas DataFrame, parsing the column 'raceDate' as a datetime object rather than plain text (e.g., 2023-03-05)

    results_page = retry(lambda: api.get_race_results(season=year)) # calling the Ergast API with the retry helper and saving the results object into a variable

    
    print(type(results_page)) # checking the type of the response object returned by the ergast API (should be a fastf1.ergast.RaceResultsPage object)
    print(f"Type of results_page.description: {type(results_page.description)}") # Type of the metadata attribute of the results_page object
    print(f"Type of results_page.content: {type(results_page.content)}") # Type of the race-level results data attribute

    print(f"Metadata inspection: {results_page.description.head()}")
    print(f"Length of results_page.content: {len(results_page.content)}")

    print(f"Type of the first race-level result: {type(results_page.content[0])}") 
    print(f"First race-level result inspection: {results_page.content[0].head()}")

    chunks = []
    received = 0

    while True:
        for (_, meta), result in zip(results_page.description.iterrows(), results_page.content): # accessing the description (metadata) and content attributes (the race-level data and the race results data)
            results_df = pd.DataFrame(result).copy() # save the race results into a dataframe and make a copy of it to avoid overwriting the original data

            for col_name in ['season', 'round', 'raceName', 'raceDate', 'circuitId']: # iterate over each of the metadata columns
                results_df[col_name] = meta[col_name] # add the metadata columns to the results dataframe (breadcasting the metadata values to all rows in the results dataframe)

            chunks.append(results_df) # append the paginated results dataframe to the chunks list
            received += len(results_df) # increment the received counter by the number of rows in the results dataframe

        if received >= results_page.total_results: # Break the loop if the number of recieved results is greater than or equal to the total number of results available in the API response
            break

        try:
            time.sleep(0.5) # pause running the program for 0.5 seconds to avoid reaching the API rate limit
            results_page = retry(results_page.get_next_result_page)
        except ValueError as exception:
            if "No next page" in str(exception):
                break
            raise

        if not chunks:
            return pd.DataFrame() # return an empty dataframe if no results for the specified season were found

        results_df = pd.concat(chunks, ignore_index=True).drop_duplicates(subset=['season', 'round', 'driverId'])
        results_df.to_csv(path, index=False)

        return results_df

# Retrieving the race schedule
schedule = retry(lambda: api.get_race_schedule(season=target_year))
austin = schedule.loc[schedule['cirquitId'].eq('americas')].copy()

# Raise a value error if no results were found for the Americas circuit in the target season
if len(austin) != 1:
    raise ValueError(f"No race found for the Americas circuit for the {target_year} season. Check the race schedule and target_year")

target_race = austin.iloc[0]