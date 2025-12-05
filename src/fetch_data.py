import fastf1
import pandas as pd
import os

# Enable cache
fastf1.Cache.enable_cache('../data/cache')

year = 2025
grand_prix = ['Australia', 'China', 'Japan', 'Bahrain', 'Saudi Arabia', 'Miami', 'Emilia-Romagna', 'Monaco', 'Spain', 'Canada', 'Austria', 'Great Britain', 'Belgium', 'Hungary', 'Netherlands', 'Italy', 'Azerbaijan', 'Singapore', 'United States', 'Mexico', 'Brazil', 'Las Vegas', 'Qatar', 'Abu Dhabi']
session_types = ['Practice1', 'Practice2', 'Practice3', 'Qualifying', 'Race']
