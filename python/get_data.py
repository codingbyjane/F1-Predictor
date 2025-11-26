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
rus_laps = laps.pick_drivers(['63']) # George Russel

ant_laps = ant_laps.reset_index(drop=True)
ver_laps = ver_laps.reset_index(drop=True)
lec_laps = lec_laps.reset_index(drop=True)
rus_laps = rus_laps.reset_index(drop=True)

# retrieving the fastest lap for each driver
fastest_ant = ant_laps.sort_values(by='LapTime').head(1)
fastest_lec = lec_laps.sort_values(by='LapTime').head(1)
fastest_ver = ver_laps.sort_values(by='LapTime').head(1)
fastest_rus = rus_laps.sort_values(by='LapTime').head(1)

# retrieve the fastest lap per driver
fastest_per_driver = laps.groupby('Driver')['LapTime'].min()

# the fastest general lap in the session
session_best = laps.pick_fastest()

ant_lap48 = ant_laps[ant_laps['LapNumber'] == 48].iloc[0]
lec_lap43 = lec_laps[lec_laps['LapNumber'] == 43].iloc[0]
ver_lap50 = ver_laps[ver_laps['LapNumber'] == 50].iloc[0]
rus_lap50 = rus_laps[rus_laps['LapNumber'] == 50].iloc[0]

# getting telemetry for that lap
ant_lap48_tel = ant_lap48.get_telemetry()

ant_speed = ant_lap48_tel['Speed']

# retrieve all laps on soft tyres
soft_laps = laps[laps['Compound'] == 'SOFT']

# retrieve average lap time per stint
laps_avg = laps.groupby(['Driver', 'Stint'])['LapTime'].mean()

# print(ant_laps[['LapNumber', 'LapTime', 'Position']].tail(35))
# print(ant_speed.head())

# checking out plotting for russel

# getting telemetry for 50th lap
rus_lap50_tel = rus_lap50.get_car_data().add_distance()

import matplotlib.pyplot as plt
import fastf1.plotting

fastf1.plotting.setup_mpl(color_scheme='fastf1')

plt.figure(figsize=(12, 6))
plt.plot(rus_lap50_tel['Distance'], rus_lap50_tel['Speed'])

plt.title("Russel - Speed vs Distance on Lap 50")
plt.xlabel("Distance (m)")
plt.ylabel("Speed (km/h)")
plt.grid = True

# plt.show()

rus_lap_time = rus_laps['LapTime'].iloc[0] # access the time of the first lap
rus_lap_seconds = rus_lap_time.total_seconds() 
rus_lap_times_seconds = rus_laps['LapTime'].dt.total_seconds() # gets all lap times as seconds
rus_positions = rus_laps['Position']


# Experimenting with plotting - Leclerc vs Antonelli comparison

# Convert timedelta to seconds for plotting
lec_lap_time_scd = lec_laps['LapTime'].dt.total_seconds()
ant_lap_time_scd = ant_laps['LapTime'].dt.total_seconds()

fastf1.plotting.setup_mpl(color_scheme='fastf1')

# Plot
plt.figure(figsize=(12,6))
plt.plot(lec_laps['LapNumber'], lec_lap_time_scd, marker='o', label='Leclerc')
plt.plot(ant_laps['LapNumber'], ant_lap_time_scd, marker='x', label='Antonelli')

plt.xlabel('Lap Number')
plt.ylabel('Lap Time (seconds)')
plt.title('Lap Time Comparison: Leclerc vs Antonelli')
plt.grid = True
plt.legend()

#plt.show()