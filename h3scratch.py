import h3
import pandas as pd
import folium  
import branca.colormap as cm

lat = 40.7128
lng = -74.0060
h3_index = h3.latlng_to_cell(lat, lng, 10)

print(f"H3 index: {h3_index}")

lat_lng = h3.cell_to_latlng(h3_index)
print(f"Latitude/Longitude: {lat_lng}")

boundary = h3.cell_to_boundary(h3_index)
print(f"Boundary: {boundary}")

m = folium.Map(location=[lat, lng], zoom_start=16)

folium.Polygon(locations=boundary, color='blue', fill=True, fill_color='blue', fill_opacity=0.4).add_to(m)

m.save('maps/hexagrid.html')