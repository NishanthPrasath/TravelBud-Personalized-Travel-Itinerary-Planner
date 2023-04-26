# from backend import schema
from fastapi import FastAPI,Depends, APIRouter
import sqlite3
import os
import pandas as pd
from passlib.context import CryptContext
# from backend import access_token
# from backend import oauth2
from fastapi.security import OAuth2PasswordRequestForm
# import boto3
import requests
from pydantic import BaseModel
from dotenv import load_dotenv
import googlemaps
from itertools import combinations
import json

load_dotenv()

# clientlogs = boto3.client('logs',
# region_name= "us-east-1",
# aws_access_key_id=os.environ.get('AWS_LOG_ACCESS_KEY'),
# aws_secret_access_key=os.environ.get('AWS_LOG_SECRET_KEY'))

cwd = os.getcwd()
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

class top_attractions(BaseModel):
    city: str
    types: str

class optimal_pairs(BaseModel):
    locations: list

# @app.post('/login')
# async def read_root(login_data: OAuth2PasswordRequestForm = Depends()):
#     # try:
#     database_file_name = "travel_app.db"
#     database_file_path = os.path.join(project_dir, os.path.join('backend/',database_file_name))
#     db = sqlite3.connect(database_file_path)
#     user= pd.read_sql_query('SELECT * FROM Users where username="{}"'.format(login_data.username), db)
#     if len(user) == 0:
#         data = {"message": "User not found", "status_code": "404"}
#     else:
#         pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
#         if pwd_cxt.verify(login_data.password, user['hashed_password'][0]):
#             print("password verified")
#             data = {'message': 'Username verified successfully', 'status_code': '200'}
#             accessToken = access_token.create_access_token(data={"sub": str(user['username'][0])})
#             data = {'message': "Success",'access_token':accessToken,'service_plan': user['service_plan'][0],'status_code': '200'}
#         else:
#             data = {'message': 'Password is incorrect','status_code': '401'}
#     # except Exception as e:
#     #     data = {'message': str(e),'status_code': '500'}
#     return data

@app.post('/GetTopAttractions')
async def get_top_attractions(data: top_attractions):
    API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
    attractions_lst = []

    # define parameters for API request
    radius = "10000"  # in meters
    # types = 'tourist_attraction|amusement_park|park|point_of_interest|establishment'

    # build API request URL
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={data.city}&radius={radius}&types={data.types}&key={API_KEY}"

    # send API request and get JSON response
    response = requests.get(url).json()

    # get top 10 attractions by rating
    attractions = sorted(response["results"], key=lambda x: x.get("rating", 0), reverse=True)[:10]

    # print names and addresses of top 10 attractions
    for attraction in attractions:
        attractions_lst.append(attraction["name"])

    response_data = {'data': attractions_lst,
            'status_code': '200'}

    return response_data

@app.post('/FindOptimalPairs')
async def find_optimal_pairs(data: optimal_pairs):

    gmaps = googlemaps.Client(key= os.environ.get('GOOGLE_MAPS_API_KEY'))

    location_pairs = list(combinations(data.locations, 2))

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

    if len(data.locations) % 2 == 1:
        left_out_location = set(data.locations) - visited_locations
        if left_out_location:
            str_data = (
                "Optimal pairs:\n"
                + "\n".join(
                    [f"{pair[0]} and {pair[1]}: {distance} km" for pair, distance in optimal_pairs]
                )
                + f"\nLeft out location: {left_out_location.pop()}"
            )
    str_data = (
        "Optimal pairs:\n"
        + "\n".join([f"{pair[0]} and {pair[1]}: {distance} km" for pair, distance in optimal_pairs])
    )

    response_data = {'data': str_data,
            'status_code': '200'}
    
    return response_data

