import googlemaps
from itertools import combinations
import os
from dotenv import load_dotenv


load_dotenv()

def find_optimal_pairs(locations):

    gmaps = googlemaps.Client(key= os.environ.get('GOOGLE_MAPS_API_KEY'))

    location_pairs = list(combinations(locations, 2))

    distances = {}
    for pair in location_pairs:
        distance = gmaps.distance_matrix(pair[0], pair[1])['rows'][0]['elements'][0]['distance']['value'] / 1000
        distances[pair] = distance

    # Sort distances by value
    sorted_distances = sorted(distances.items(), key=lambda x: x[1])

    # Greedy approach to find optimal pairs
    visited_locations = set()
    optimal_pairs = []

    for pair, distance in sorted_distances:
        if pair[0] not in visited_locations and pair[1] not in visited_locations:
            optimal_pairs.append((pair, distance))
            visited_locations.add(pair[0])
            visited_locations.add(pair[1])

    if len(locations) % 2 == 1:
        left_out_location = set(locations) - visited_locations
        if left_out_location:
            return (optimal_pairs, left_out_location.pop())
    return (optimal_pairs, None)

locations = ['Boston Common MA', 'Seaport Boston', 'MFA', 'Flume New Hampshire', 'White Mountains New Hampshire']
optimal_pairs, left_out_location = find_optimal_pairs(locations)
print("Optimal pairs:")
for pair, distance in optimal_pairs:
    print(f"{pair[0]} and {pair[1]}: {distance} km")
if left_out_location:
    print(f"Left out location: {left_out_location}")

