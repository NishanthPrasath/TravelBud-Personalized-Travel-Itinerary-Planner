import requests
import os
from dotenv import load_dotenv

load_dotenv()



def get_top_attractions(city_name):
    API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
    attractions_lst = []

    # define parameters for API request
    radius = "10000"  # in meters
    types = 'tourist_attraction|amusement_park|park|point_of_interest|establishment'

    # build API request URL
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={city_name}&radius={radius}&types={types}&key={API_KEY}"

    # send API request and get JSON response
    response = requests.get(url).json()

    # get top 10 attractions by rating
    attractions = sorted(response["results"], key=lambda x: x.get("rating", 0), reverse=True)[:10]

    # print names and addresses of top 10 attractions
    for attraction in attractions:
        attractions_lst.append(attraction["name"])

    return attractions_lst


get_top_attractions("New York City")
