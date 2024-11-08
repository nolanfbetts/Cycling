import h3
import pandas as pd

incident_data = pd.read_csv('./data/CompleteDataSetMVC.csv')
weather_data = pd.read_csv('./data/WeatherData.csv')

#return rows where NUMBER OF CYCLIST INJURED is not 0 or NUMBER OF CYCLIST KILLED is not 0
# incident_data = incident_data[(incident_data['NUMBER OF CYCLIST INJURED'] != 0) | (incident_data['NUMBER OF CYCLIST KILLED'] != 0)] 

# add a column datatime to incident_data of the format 'YYYY-MM-DDTHH:MM:SS' and round the time to the nearest hour using the columns CRASH DATE and CRASH TIME
incident_data['CRASH DATE'] = pd.to_datetime(incident_data['CRASH DATE'])
incident_data['CRASH TIME'] = pd.to_datetime(incident_data['CRASH TIME'], format='%H:%M').dt.time
incident_data['datetime'] = incident_data.apply(lambda row: pd.Timestamp.combine(row['CRASH DATE'], row['CRASH TIME']), axis=1)
incident_data['datetime'] = incident_data['datetime'].dt.round('H')
incident_data['datetime'] = incident_data['datetime'].dt.strftime('%Y-%m-%dT%H:%M:%S')

# get weather data for the same date and time as the incident data and add it to incident_data
weather_data['datetime'] = pd.to_datetime(weather_data['datetime'])
weather_data['datetime'] = weather_data['datetime'].dt.round('H')
weather_data['datetime'] = weather_data['datetime'].dt.strftime('%Y-%m-%dT%H:%M:%S')

# merge incident_data with weather_data on the datetime column
merged_data = pd.merge(incident_data, weather_data, on='datetime', how='left')

# replace incident_data with merged_data
incident_data = merged_data

# add a 'DAY OF WEEK' column to incident_data using the datatime column
incident_data['datetime'] = pd.to_datetime(incident_data['datetime'])
incident_data['DAY OF WEEK'] = incident_data['datetime'].dt.day_name()

incident_data = incident_data.dropna(subset=['LATITUDE', 'LONGITUDE'])

def find_h3_and_boundaries(row, resolution=10):
    lat = row['LATITUDE']
    lng = row['LONGITUDE']
    h3_index = h3.latlng_to_cell(lat, lng, resolution)
    boundaries = h3.cell_to_boundary(h3_index)
    return pd.Series([h3_index, boundaries])

incident_data[['H3_INDEX', 'BOUNDARIES']] = incident_data.apply(find_h3_and_boundaries, axis=1)


print(incident_data.head())
print(incident_data.shape)
print(incident_data.info())

incident_data.to_csv('./data/processed_data_all.csv', index=False)