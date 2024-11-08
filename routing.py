import folium
import osmnx as ox
import networkx as nx
import pandas as pd

# Set your start and end coordinates
trip_data = pd.read_csv('./data/citibike.csv')

for index, row in trip_data.iterrows():
    if(index%1000 == 0):
        print(index)
    start_location = (row['start_lat'], row['start_lng'])  # Example: New York (Latitude, Longitude)
    end_location = (row['end_lat'], row['end_lng'])    # Another point in New York

    # Download the road network around your location
    G = ox.graph_from_point(start_location, dist=3000, network_type='bike')  # 'drive' for driving routes

    # Find the nearest nodes to the start and end points
    orig_node = ox.distance.nearest_nodes(G, start_location[1], start_location[0])
    dest_node = ox.distance.nearest_nodes(G, end_location[1], end_location[0])

    # Find the shortest path between these nodes using NetworkX
    route = nx.shortest_path(G, orig_node, dest_node, weight='length', method='djikstra')

    # Get the coordinates of the route
    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]


# Create a folium map centered around the starting point
m = folium.Map(location=start_location, zoom_start=13)

# Add the route to the map
folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.7).add_to(m)

# Add start and end markers
folium.Marker(start_location, tooltip="Start", icon=folium.Icon(color="green")).add_to(m)
folium.Marker(end_location, tooltip="End", icon=folium.Icon(color="red")).add_to(m)

# Display the map
m.save('route_map.html')

