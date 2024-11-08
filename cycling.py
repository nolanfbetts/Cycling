import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from folium import plugins
import folium
import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import h3
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import h3
import pandas as pd
import folium  
import branca.colormap as cm





def load_data():
    incident_data = pd.read_csv('./data/CompleteDataSetMVC.csv')
    weather_data = pd.read_csv('./data/WeatherData.csv')

    #return rows where NUMBER OF CYCLIST INJURED is not 0 or NUMBER OF CYCLIST KILLED is not 0
    incident_data = incident_data[(incident_data['NUMBER OF CYCLIST INJURED'] != 0) | (incident_data['NUMBER OF CYCLIST KILLED'] != 0)] 

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
    return incident_data


def create_day_of_week_plot(incident_data, kind='bar'):
    # create bar plot of the number of incidents by day of the week
    incident_counts = incident_data['DAY OF WEEK'].value_counts().sort_index()
    incident_counts.plot(kind=kind)
    days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    incident_counts = incident_counts.reindex(days_of_week)
    plt.gca().set_xticklabels(incident_counts.index, rotation=45, ha='right')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Incidents')
    plt.title('Number of Incidents by Day of the Week')
    plt.show()
    
# TODO: Create a more generic function
'''
Creates a plot of the number of incidents by year
- Incident data is a DataFrame containing the incident data
- kind is the type of plot to create (e.g., 'line', 'bar')
'''
def create_yearly_plot(incident_data, kind='line'):
    # create line plot of the number of incidents by year
    incident_data['CRASH DATE'] = pd.to_datetime(incident_data['CRASH DATE'])
    incident_data['Year'] = incident_data['CRASH DATE'].dt.year
    incident_counts = incident_data['Year'].value_counts().sort_index()
    incident_counts.plot(kind=kind)
    plt.xlabel('Year')
    plt.ylabel('Number of Incidents')
    plt.title('Number of Incidents by Year')
    plt.show()
'''
Creates a plot of the number of incidents by day
- Incident data is a DataFrame containing the incident data
- kind is the type of plot to create (e.g., 'line', 'bar')
'''
def create_time_of_day_plot(incident_data, kind='bar'):
    # create bar plot of the number of incidents by time of day
    incident_data['datetime'] = pd.to_datetime(incident_data['datetime'])
    incident_data['Hour'] = incident_data['datetime'].dt.hour
    incident_counts = incident_data['Hour'].value_counts().sort_index()
    incident_counts.plot(kind=kind)
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Incidents')
    plt.title('Number of Incidents by Time of Day')
    plt.show()
'''
Creates a plot of the number of incidents by month
- Incident data is a DataFrame containing the incident data
- kind is the type of plot to create (e.g., 'line', 'bar')
'''
def create_monthly_plot(incident_data, kind='line'):
    # create line plot of the number of incidents by month
    incident_data['datetime'] = pd.to_datetime(incident_data['datetime'])
    incident_data['Month'] = incident_data['datetime'].dt.month
    incident_counts = incident_data['Month'].value_counts().sort_index()
    incident_counts.plot(kind=kind)
    # make X Labels more readable by changing them to month names
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    incident_counts = incident_counts.reindex(months)
    plt.gca().set_xticklabels(incident_counts.index, rotation=45, ha='right')
    plt.xlabel('Month')
    plt.ylabel('Number of Incidents')
    plt.title('Number of Incidents by Month')
    plt.show()
    
def create_heatmap_day_of_week_vs_time_of_day(incident_data):
    # create a heatmap of the number of incidents by day of the week and time of day
    incident_data['datetime'] = pd.to_datetime(incident_data['datetime'])
    incident_data['Hour'] = incident_data['datetime'].dt.hour
    day_of_week_time_of_day = incident_data.groupby(['DAY OF WEEK', 'Hour']).size().unstack()
    day_of_week_time_of_day = day_of_week_time_of_day.reindex(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
    plt.figure(figsize=(12, 10))
    sns.heatmap(day_of_week_time_of_day, cmap="coolwarm", cbar=True)
    plt.xlabel('Hour of the Day')
    plt.ylabel('Day of the Week')
    plt.title('Number of Incidents by Day of the Week and Time of Day')
    plt.show()
'''
Creates a covariance matrix of the numerical columns in the incident data
- incident_data is a DataFrame containing the incident data
'''
def create_correlation_matrix(incident_data):
    # Select only numerical columns for the covariance matrix
    numerical_data = incident_data.select_dtypes(include=[np.number])
    # Scale numerical data
    scaler = StandardScaler()
    numerical_data = pd.DataFrame(scaler.fit_transform(numerical_data), columns=numerical_data.columns)
    # Compute the covariance matrix
    correlation_matrix = numerical_data.corr()
    
    # Display the covariance matrix as a heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
    plt.title("Covariance Matrix of Incident Data Features")
    plt.show()
    
    return correlation_matrix 
'''
Create Heatmap of the incidents
'''
def create_heatmap(incident_data):
# Remove rows where dropoff_lat or dropoff_lng are NaN
    data = incident_data.dropna(subset=['LATITUDE', 'LONGITUDE'])

    # Create list of coordinates
    coord = []
    for lat, lng in zip(data['LATITUDE'].values, data['LONGITUDE'].values):
        coord.append([lat, lng])

    # Create the map
    map = folium.Map(
        location=[40.7128, -74.0060],
        tiles='OpenStreetMap',
        zoom_start=7,
        control_scale=True
    )

    # Add heat map layer
    map.add_child(plugins.HeatMap(coord, radius=15, blur=10))

    # Show the map
    map.save('maps/heatmap.html')
'''
Setting up the data and previewing it
'''    
incident_data = load_data()
# print the first 5 rows of incident_data
print(incident_data.head())
# print incident_data info
print(incident_data.info())

'''
 Simple Plotting options for the data
'''
# create_day_of_week_plot(incident_data=incident_data, kind='bar')
# create_yearly_plot(incident_data=incident_data, kind='line')
# create_time_of_day_plot(incident_data=incident_data, kind='bar')
# create_monthly_plot(incident_data=incident_data, kind='bar')
# create_heatmap_day_of_week_vs_time_of_day(incident_data=incident_data)


# Generate and display the covariance matrix
# cov_matrix = create_correlation_matrix(incident_data)
create_heatmap(incident_data)

def find_h3_and_boundaries(row, resolution=10):
    lat = row['LATITUDE']
    lng = row['LONGITUDE']
    h3_index = h3.latlng_to_cell(lat, lng, resolution)
    boundaries = h3.cell_to_boundary(h3_index)
    return pd.Series([h3_index, boundaries])

def create_hexamap(incident_data):
    data = incident_data.dropna(subset=['LATITUDE', 'LONGITUDE'])
    data[['H3_INDEX', 'BOUNDARIES']] = data.apply(find_h3_and_boundaries, axis=1)
    incident_counts = data.groupby('H3_INDEX').size().reset_index(name='Count')
    incident_counts = incident_counts.merge(data[['H3_INDEX', 'BOUNDARIES']].drop_duplicates(), on='H3_INDEX', how='left')
    
    m = folium.Map(location=[40.7128, -74.0060], zoom_start=10, tiles='cartodbpositron')
    # colormap = cm.LinearColormap(colors=['#ffcccc', '#ff0000'], vmin=incident_counts['Count'].min(), vmax=100)
        # Define a LinearColormap for a heat map effect
    colormap = cm.LinearColormap(
        colors=['#ffffcc', '#ffeda0', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#b10026'],
        vmin=incident_counts['Count'].min(),
        vmax=50,
        caption='Incident Density'
    )
    for _, row in incident_counts.iterrows():
        folium.Polygon(locations=row['BOUNDARIES'], color=colormap(row['Count']), fill=True, fill_opacity=0.7, popup=f'Count: {row['Count']}').add_to(m)
    colormap.add_to(m)
    print(data.head())
    print(data.info())
    # list of most frequent h3 indexes
    print(incident_counts.sort_values(by='Count', ascending=False).head())
    # number of unique h3 indexes
    print(incident_counts['H3_INDEX'].nunique())
    
    m.save('maps/hexamap.html')
# Display map

create_hexamap(incident_data)
