from collections import defaultdict, deque

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

# Define dictionaries to store recent history for drivers, teams, and circuits
drivers = defaultdict(lambda: deque(maxlen=5))
teams = defaultdict(lambda: deque(maxlen=5))
circuits = defaultdict(lambda: deque(maxlen=5))