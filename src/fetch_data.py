import fastf1
import pandas as pd
import os
from pathlib import Path

# Enable cache
fastf1.Cache.enable_cache('../data/cache')

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"

year = 2025
grand_prix = ['Australia', 'China', 'Japan', 'Bahrain', 'Saudi Arabia', 'Miami', 'Emilia-Romagna', 'Monaco', 'Spain', 'Canada', 'Austria', 'Great Britain', 'Belgium', 'Hungary', 'Netherlands', 'Italy', 'Azerbaijan', 'Singapore', 'United States', 'Mexico', 'Brazil', 'Las Vegas', 'Qatar', 'Abu Dhabi']
session_types = ['FP1', 'FP2', 'FP3', 'Q', 'R', 'SS', 'Sprint']

# drivers_to_fetch = ['1', '63', '12', '16', '55', '6', '27', '44', '31', '87', '14', '22', '10', '30', '43', '23', '5', '18', '4', '81']

for idx, race in enumerate(grand_prix): # Loop over each race name in the grand_prix list
        
        # print(f"Loading {year} - {idx+1:02d} - {race} - {session_type}")

        print(f"\n=== {year} - {idx+1:02d} - {race} ===")
        # Output:
        # === 2025 - 04 - Bahrain ===  

        # session = fastf1.get_session(year, race, session_type)
        # session.load()

        # Get actual sessions for this event
        event = fastf1.get_event(year, race)
        valid_sessions = event.sessions # e.g. ['FP1','SS','Sprint','Q','R']

        for session_type in valid_sessions:
                print(f" Loading: {race} - {session_type}")
