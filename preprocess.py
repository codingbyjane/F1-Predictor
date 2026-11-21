# Importing dependencies
from pathlib import Path

import pandas as pd
import numpy as np

import time
from datetime import timezone, datetime

# FastF1 API for data retrieval
import fastf1
from fastf1.ergast import Ergast

from IPython.display import display

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

    # Inspect the columns in both returned attributes
    print(f"Columns in the metadata attribute: {results_page.description.columns}")
    print(f"Columns in the first result of the race-level data attribute: {results_page.content[0].columns}")

    # Check the total number of results available in the API response
    print(f"Total number of results available in one API response: {results_page.total_results}")

    chunks = []
    received = 0

    while True:
        for (_, meta), result in zip(results_page.description.iterrows(), results_page.content): # accessing the description (metadata) and content attributes (the race-level data and the race results data). This zips the inner metadata tuple (index, pd.series) with the results dataframe
            results_df = pd.DataFrame(result).copy() # save the race-level results into a dataframe and make a copy of it to avoid overwriting the original data

            for col_name in ['season', 'round', 'raceName', 'raceDate', 'circuitId']: # iterate over each of the metadata columns
                results_df[col_name] = meta[col_name] # add the metadata columns to the race-level results dataframe (broadcasting the scalar metadata values to all rows in the results dataframe)

            chunks.append(results_df) # append the paginated race-level results dataframes to the chunks list
            received += len(results_df) # increment the counter by the number of rows in the results dataframe

        if received >= results_page.total_results: # Break the loop if the number of recieved results is greater than or equal to the total number of results available in the API response (how many results match the season query overall, not just how many are on that page). 'total_results' is a property of the ErgastResponseMixin class that returns the total number of results available for the specified season
            break

        # Get the next results page and handle the case where there are no more results available
        try:
            time.sleep(0.5) # pause running the program for 0.5 seconds to avoid reaching the API rate limit
            results_page = retry(results_page.get_next_result_page)
        except ValueError as exception:
            if "No next page" in str(exception):
                break
            raise

    if not chunks: # if the chunks list is empty (not chunks = False)
        return pd.DataFrame() # return an empty dataframe if no results for the specified season were found

    results_df = pd.concat(chunks, ignore_index=True).drop_duplicates(subset=['season', 'round', 'driverId']) # concat() stacks the dataframes vertically, ignore original indeces
    results_df.to_csv(path, index=False)

    return results_df


# Retrieving the race schedule for the target year
schedule = retry(lambda: api.get_race_schedule(season=target_year))
print(f"\nType of the returned schedule attribute: {type(schedule)}")

# Filtrering the schedule for the Americas circuit (Austin GP)
austin = schedule.loc[schedule['circuitId'].eq('americas')].copy() # Equivalent to schedule[schedule['cirquitId'] == 'americas']. The .loc method is label-based indexing

# Raise a value error if no results were found for the Americas circuit in the target season or there are more than one matched result for the race
if len(austin) != 1:
    raise ValueError(f"No valid race found in the Americas circuit for the {target_year} season. Check the race schedule and target year variable. Found {len(austin)} races instead of 1.")

target_race = austin.iloc[0] # Get the first row of the matched dataframe (there should only be one row for the Americas circuit in the target season). the .iloc method is position-based indexing

# Target race date inspection
print(f"Target race date: {target_race['raceDate']}")
print(f"Type of the target race date: {type(target_race['raceDate'])}")
print(f"Inspect of the target race date value is a Pandas Timestamp object: {target_race['raceDate'].tz}\n")

target_date = pd.Timestamp(target_race['raceDate'].tz_localize(None)).normalize() # assign the target date to a corresponding variable and the race date to a timezone-naive timestamp and normalize it to midnight

# Create an empty list to store the season results dataframes for each year (i.e., collecting previously created results_df dataframes for each year from the start year to the target year (inclusive))
season_results_frames = []

for year in range(start_year, target_year + 1): # Iterate through the years from the start year to the target year (+1 means inclusive of the target year)
    partial_results = season_results(year)

    if not partial_results.empty:
        season_results_frames.append(partial_results)
    print(f"{year}: {len(partial_results)} driver results loaded")

raw_szn_results_df = pd.concat(season_results_frames, ignore_index=True) # concatenate all the seasonal results dataframes stored in the list into a single large dataframe of raw results, ignore the original pandas indeces. By default, pd.concat() stacks DataFrames vertically (axis=0). In other words, it adds rows, not columns.

# Inspect if the 'raceDate' column is a timezone-aware datetime dtype
print(raw_szn_results_df['raceDate'].dtype)
raw_szn_results_df['raceDate'] = pd.to_datetime(raw_szn_results_df['raceDate'].dt.tz_localize(None)) # Removing the timezone information from the 'raceDate' column and converting it to timezone-naive datetime values. (.dt gives you access to date/time-specific operations on that Series)

today = pd.Timestamp(datetime.now(timezone.utc)).date()

'''history_df = raw_szn_results_df.loc[(raw_szn_results_df['raceDate'] < target_date) & (raw_szn_results_df['raceDate'] < today)].copy()'''

history_df = raw_szn_results_df.loc[(raw_szn_results_df['raceDate'] < target_date)].copy() # Filter the raw seasonal results dataframe to include only historical data preceding the target race date and store its copy in a corresponding variable


history_df['position'] = pd.to_numeric(history_df['position'], errors='raise')
history_df['points'] = pd.to_numeric(history_df['points'], errors='raise')

history_df = history_df.sort_values(['raceDate', 'season', 'round', 'position'])

# Check if there are any duplicated driver results found. Pandas .duplicated() returns a boolean series indicating whether each row is a duplicate of a previous row based on the specified subset of columns. The .any() method checks if any of the values in the boolean series are True, indicating that there are duplicates present. If duplicates are found, an AssertionError is raised.
assert not history_df.duplicated(['season', 'round', 'driverId']).any(), "Duplicate driver results found for the same race. Check the data for inconsistencies."

# Aggregate the number of entrants and winners for each race in the historical data
race_checks = history_df.groupby(['season', 'round']).agg(
    entrants=('driverId', 'size'), winners=('position', lambda x: x.eq(1).sum())
)

# Check if any races have fewer than 18 entrants. The .ge() method checks if each value in the 'entrants' column is greater than or equal to 18, and the .all() method checks if all values in the resulting boolean series are True. If any race has fewer than 18 entrants, an AssertionError is raised.
assert race_checks['entrants'].ge(18).all(), "Incomplete race data. Some races have fewer than 18 entrants. Check the data for inconsistencies."
assert race_checks['winners'].eq(1).all(), "Invalid race data. Each race has to have exactly one winner. Check the data for inconsistencies."
assert history_df['season'].max() == target_year, "No current season data found. Check data availability for the target year."

print(f"\nTarget race: {target_race['raceName']} - {target_date.date()}")
print(f"Latest historical race before the target date: {history_df['raceDate'].max().date()}")

# Access the maximum element in the history_df dataframe through the 'raceDate' label
latest_race = history_df.loc[history_df['raceDate'].eq(history_df['raceDate'].max())].copy()
race_preview = latest_race.assign(Driver=latest_race.givenName + " " + latest_race.familyName)

display(race_preview[['Driver', 'constructorName', 'position', 'points']].head(5)
        .rename(columns={
            'constructorName' : 'Team',
            'position' : 'Finished',
            'points' : 'Points'
        })
        .reset_index(drop=True)
        )