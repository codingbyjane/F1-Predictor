from collections import defaultdict, deque

import numpy as np

# Define the features for the model
FEATURES = [
    'driver_finish_5',
    'driver_points_5',
    'driver_win_rate_5',
    'driver_podium_rate_5',
    'team_points_5',
    'team_win_rate_5',
    'circuit_finish_3',
    'circuit_win_rate_3',
    'driver_history_count'
]

# Define dictionaries to store recent history for drivers, teams, and circuits. defaultdict automatically creates a value for a new key
drivers = defaultdict(lambda: deque(maxlen=5))
teams = defaultdict(lambda: deque(maxlen=5))
circuits = defaultdict(lambda: deque(maxlen=5))

def average(records, column):
    return float(np.mean([row[column] for row in records])) if records else np.nan