# imports
import sys
sys.path.append('../../')
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dont_add.config.api_key import weather_key as wKey
import requests
from scipy.stats import linregress
from pprint import pprint
from citipy import citipy
import random
import datetime

# Save a Pandas DF to a csv with a timestamp on it
# you nees a base path, the dataframe and the name you want thefile to be called
def saveTimeStamped(df, base_path, name):
    name = '/' + name
    time_stamp = datetime.date.today()
    file_name = f'{name}_{time_stamp}'
    outpath = base_path + file_name
    df.to_csv(outpath, index=False)
    

# using a dict of lists for lats and lngs, it makes a list of city names
def makeCitiesList(country_coords):
    
    # Range of latitudes and longitudes for the set confines
    lat_range = (country_coords['lat'][0], country_coords['lat'][1])
    lng_range = (country_coords['lng'][0], country_coords['lng'][1])

    # List for holding lat_lngs and cities
    lat_lngs = []
    cities = []

    # Create a set of random lat and lng combinations
    lats = np.random.uniform(low=lat_range[0], high=lat_range[1], size=1500)
    lngs = np.random.uniform(low=lng_range[0], high=lng_range[1], size=1500)
    lat_lngs = zip(lats, lngs)

    # Identify nearest city for each lat, lng combination
    for lat_lng in lat_lngs:
        city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name

        # If the city is unique, then add it to a our cities list
        if city not in cities:
            cities.append(city)

    # Print the city count to confirm sufficient count
    len(cities)
    return(cities)


# using a list of city names this pings the weather api to gather the needed data
# makes a pandas dataframe and outputs it as a csv
def collectData(cities, filename):
    
    # Lists to store data into
    cur_temps = []
    min_temps = []
    max_temps = []
    feel_temps = []
    humidities = []
    cloudinessess = []
    windSpeeds = []
    cityLats = []
    cityLngs = []
    dates = []
    countries = []
    names = []
    pressures = []
    
    # loop to get the data for each city
    units = 'imperial'
    count = 1
    print('Beginning Data Retrieval')
    print('--------------------------------------')
    for city in cities:
        params = {'q' : city, 'appid': wKey, 'units' : units}
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={wKey}&units=imperial'
        response = requests.get(url).json()
        print(f'Attempting to save data for {city} : (number{count})')
        try:
            names.append(response['name'])
            max_temps.append(response['main']['temp_max'])
            cur_temps.append(response['main']['temp'])
            min_temps.append(response['main']['temp_min'])
            feel_temps.append(response['main']['feels_like'])
            humidities.append(response['main']['humidity'])
            cloudinessess.append(response['clouds']['all'])
            windSpeeds.append(response['wind']['speed'])
            cityLats.append(response['coord']['lat'])
            cityLngs.append(response['coord']['lon'])
            dates.append(response['dt'])
            countries.append(response['sys']['country'])
            pressures.append(response['main']['pressure'])
        except KeyError:
            print(f'failed to find all info for {city}, skipping remaining info')
        count += 1
    print('--------------------------------------')
    print('Data Retrieval Complete')
    print('--------------------------------------')
    
    # make Pandas DF for collected data
    base_df_dict = {
        'City' : names,
        'Cloudiness' : cloudinessess,
        'Country' : countries,
        'Date' : dates,
        'Humidity' : humidities,
        'Lat' : cityLats,
        'Lng' : cityLngs,
        'Current Temp' : cur_temps,
        'Max Temp' : max_temps,
        'Min Temp' : min_temps,
        'Feels Like Temp' : feel_temps,
        'Wind Speed' : windSpeeds,
        'Pressure' : pressures}

    base_df = pd.DataFrame(base_df_dict)
    usa_base_df = base_df[base_df['Country'] == 'US'].reset_index(drop=True)
    usa_base_df
    
    saveTimeStamped(df=base_df, base_path=out_table_path_base, name=filename)
