import fastf1
import pandas as pd
import matplotlib.pyplot as plt

# Enable caching (saves downloaded data to disk for future use)
fastf1.Cache.enable_cache('../data/cache')

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

ver_best_lap = ver_laps[ver_laps['LapTime'] == ver_laps['LapTime'].min()]

# print(fastest_ver, ver_best_lap) the output is absolutely identical

ver_valid = ver_laps[ver_laps['Deleted'] == False] # find all valid laps
ver_deleted = ver_laps[ver_laps['Deleted'] == True] # find all deleted laps

ant_s1_fastest = ant_laps[ant_laps['Sector1Time'] == ant_laps['Sector1Time'].min()] # fastest lap in sector 1
ant_s2_fastest = ant_laps[ant_laps['Sector2Time'] == ant_laps['Sector2Time'].min()] # fastest lap in sector 2
ant_s3_fastest = ant_laps[ant_laps['Sector3Time'] == ant_laps['Sector3Time'].min()] # fastest lap in sector 3

lec_fastest = lec_laps.pick_fastest() # extract info about the fastest Leclerc lap
ant_fastest = ant_laps.pick_fastest() # extract info about the fastest Antonelli lap

ant_lap48 = ant_laps[ant_laps['LapNumber'] == 48].iloc[0]
lec_lap43 = lec_laps[lec_laps['LapNumber'] == 43].iloc[0]
ver_lap50 = ver_laps[ver_laps['LapNumber'] == 50].iloc[0]
rus_lap50 = rus_laps[rus_laps['LapNumber'] == 50].iloc[0]

# retrieve average lap time per stint
laps_avg = laps.groupby(['Driver', 'Stint'])['LapTime'].mean()

# retrieving sector times
lec_sectors = lec_laps[['LapNumber', 'Sector1Time', 'Sector2Time', 'Sector3Time']].head()
rus_sectors = rus_laps[['LapNumber', 'Sector1Time', 'Sector2Time', 'Sector2Time']].head()

# playing around with telemetry now

# getting telemetry for fastest Antonelli lap
ant_lap48_tel = ant_lap48.get_telemetry()
ant_speed = ant_lap48_tel['Speed']

list(ant_lap48_tel.columns) # outputs: ['Date', 'SessionTime', 'DriverAhead', 'DistanceToDriverAhead', 'Time', 'RPM', 'Speed', 'nGear', 'Throttle', 'Brake', 'DRS', 'Source', 'Distance', 'RelativeDistance', 'Status', 'X', 'Y', 'Z']

# retrieve all laps on soft tyres
soft_laps = laps[laps['Compound'] == 'SOFT']

ver_hard = ver_laps[ver_laps['Compound'] == 'HARD'] # retrieve all laps on hard tyres for Verstappen
ver_medium = ver_laps[ver_laps['Compound'] == 'MEDIUM'] # retrieve all laps on medium tyres for Verstappen

# print(ant_laps[['LapNumber', 'LapTime', 'Position']].tail(35))

# smoothing GPS coordinates

ant_lap48_tel['X_smooth'] = ant_lap48_tel['X'].rolling(window=5, min_periods=1).mean()
ant_lap48_tel['Y_smooth'] = ant_lap48_tel['Y'].rolling(window=5, min_periods=1).mean()

print(ant_lap48_tel[['X', 'X_smooth', 'Y_smooth']].head(10))

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
rus_positions = rus_laps['Position'] # retrieve positions for Russel's laps


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
