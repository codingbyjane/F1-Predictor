import fastf1
import pandas as pd
import matplotlib.pyplot as plt

# Enable caching (saves downloaded data to disk for future use)
fastf1.Cache.enable_cache('../data/cache')

"""session = fastf1.get_session(2025, "Brazil", "Race")
session.load()

#print(session.drivers)

laps = session.laps #session.laps loads all laps of all drivers and saves it in the laps variable as a Pandas Dataframe

lec_laps = laps.pick_drivers(['16']) # Charles Leclerc
ant_laps = laps.pick_drivers(['12']) # Kimi Antonelli
ver_laps = laps.pick_drivers(['1']) # Max Verstappen

ant_laps = ant_laps.reset_index(drop=True)
ver_laps = ver_laps.reset_index(drop=True)

fastest_ant = ant_laps.sort_values(by='LapTime').head(1)

lec_lap5 = lec_laps[lec_laps['LapNumber'] == 5]
lec_lap5_time = lec_lap5['LapTime'].iloc[0]

#print(lec_laps.head())  first 5 laps of Leclerc
#print(ver_laps[['LapNumber', 'LapTime', 'Position']].tail(25)) 

"""

session = fastf1.get_session(2025, 'Las Vegas', 'Race')
session.load()

laps = session.laps

ant_laps = laps.pick_drivers(['12']) # Kimi Antonelli
lec_laps = laps.pick_drivers(['16']) # Charles Leclerc
ver_laps = laps.pick_drivers(['1']) # Max Verstappen

ant_laps = ant_laps.reset_index(drop=True)

# retrieving the fastest lap
fastest_ant = ant_laps.sort_values(by='LapTime').head(1)

ant_lap48 = ant_laps[ant_laps['LapNumber'] == 48].iloc[0]

# getting telemetry for that lap
ant_lap48_tel = ant_lap48.get_telemetry()

ant_speed = ant_lap48_tel['Speed']

# print(ant_laps[['LapNumber', 'LapTime', 'Position']].tail(35))
print(ant_speed.head())
