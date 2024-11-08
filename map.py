import pandas as pd
import folium
from folium import Choropleth
from folium import LinearColormap




# Load the CSV file
df = pd.read_csv('./data/CompleteDataSetMVC.csv')

# Drop rows with missing values in Latitude or Longitude
df = df.dropna(subset=['LATITUDE', 'LONGITUDE', 'ZIP CODE'])

# Filter out records where both 'NUMBER OF CYCLIST INJURED' and 'NUMBER OF CYCLIST KILLED' are 0
df = df[(df['NUMBER OF CYCLIST INJURED'] != 0) | (df['NUMBER OF CYCLIST KILLED'] != 0)]

# Print the number of records remaining after filtering
print(f"Number of records after filtering: {len(df)}")

# Calculate the total number of cyclist injured and killed
total_injured = df['NUMBER OF CYCLIST INJURED'].sum()
total_killed = df['NUMBER OF CYCLIST KILLED'].sum()

# Print the totals
print(f"Total number of cyclist injured: {total_injured}")
print(f"Total number of cyclist killed: {total_killed}")

# Group by 'ZIP CODE' to aggregate injuries and fatalities
grouped = df.groupby('ZIP CODE').agg(
    total_injured=('NUMBER OF CYCLIST INJURED', 'sum'),
    total_killed=('NUMBER OF CYCLIST KILLED', 'sum'),
).reset_index()

# Calculate total incidents
grouped['total_incidents'] = grouped['total_injured'] + grouped['total_killed']

# Load the GeoJSON file for NYC zip codes
geojson_path = './data/nyc_geo.min.json'

# Create a Folium map centered around the average coordinates
map_center = [df['LATITUDE'].mean(), df['LONGITUDE'].mean()]
m = folium.Map(location=map_center, zoom_start=5)



# Create the choropleth map
Choropleth(
    geo_data=geojson_path,
    data=grouped,
    columns=['ZIP CODE', 'total_incidents'],
    key_on='feature.properties.ZCTA5CE10',  # Adjust based on the properties in your GeoJSON
    fill_color='OrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Total Incidents',
).add_to(m)

# Add markers for each location
# for index, row in df.iterrows():
#     folium.CircleMarker(
#         location=[row['LATITUDE'], row['LONGITUDE']],
#         popup=f"Lat: {row['LATITUDE']}, Lon: {row['LONGITUDE']}",
#         radius=5,  # Set the radius of the circle
#             color='blue',  # Set the outline color
#             fill=True,
#             fill_color='blue',  # Set the fill color
#             fill_opacity=0.6,  # Set the fill opacity
#     ).add_to(m)

# Save the map to an HTML file
m.save('map.html')