import fastf1
import pandas as pd
import os

# Enable cache
fastf1.Cache.enable_cache('../data/cache')

year = 2025
grand_prix = ['Australia', 'China', 'Japan', 'Bahrain', 'Saudi Arabia', 'Miami', 'Emilia-Romagna', 'Monaco', 'Spain', 'Canada', 'Austria', 'Great Britain', 'Belgium', 'Hungary', 'Netherlands', 'Italy', 'Azerbaijan', 'Singapore', 'United States', 'Mexico', 'Brazil', 'Las Vegas', 'Qatar', 'Abu Dhabi']
session_types = ['FP1', 'FP2', 'FP3', 'Qualifying', 'Race']

# drivers_to_fetch = ['1', '63', '12', '16', '55', '6', '27', '44', '31', '87', '14', '22', '10', '30', '43', '23', '5', '18', '4', '81']

for idx, race in enumerate(grand_prix): # Loop over each race name in the grand_prix list
    for session_type in session_types:
        print(f"Loading {year} - {idx+1:02d} - {race} - {session_type}")

        session = fastf1.get_session(year, race, session_type)
        session.load()