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
import requests
from datetime import datetime, timedelta
import pandas as pd

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

class final_cost(BaseModel):
    start_date_val: str
    end_date_val: str
    num_days_val: int
    adults_number_val: int
    num_rooms_val: str
    des_id: str
    type_des: str
    type_val: str
    origin_val: str
    destination_val: str
    budget_val: int


def create_date_pairs(start_date, end_date, num_days):
    date_pairs = []
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    while current_date <= end_date:
        pair_end_date = current_date + timedelta(days=num_days-1)
        if pair_end_date > end_date:
            pair_end_date = end_date
        date_pairs.append((current_date.strftime('%Y-%m-%d'), pair_end_date.strftime('%Y-%m-%d')))
        current_date += timedelta(days=1)  

    return date_pairs[:-num_days+1]  # remove the last pair if it's incomplete

def get_hotel_cost(checkin_date, checkout_date, adults_number, type_des, id, rooms_cnt):

    url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

    querystring = {
        "checkin_date": checkin_date,
        "checkout_date": checkout_date,
        "adults_number": adults_number,
        "dest_type": type_des,
        "units": "metric",
        "order_by": "review_score", #sorting by review score and then finding the lowest price
        "dest_id": id,
        "filter_by_currency": "USD",
        "locale": "en-gb",
        "room_number": rooms_cnt,
        "page_number": "0",
        "include_adjacency": "true"
    }

    headers = {
                "X-RapidAPI-Key": os.environ.get('RAPID_API_KEY'),
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com"

    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    result = response.json()
    return result


def calculate_hotel_costs(start_date, end_date, num_days, adults_number, type_des, id, rooms_cnt):
    date_pairs = create_date_pairs(start_date, end_date, num_days)
    hotel_costs = []
    df_list = []

    for pair in date_pairs:
        checkin_date = datetime.strptime(pair[0], '%Y-%m-%d')
        checkout_date = datetime.strptime(pair[1], '%Y-%m-%d')
        response = get_hotel_cost(checkin_date.strftime('%Y-%m-%d'), checkout_date.strftime('%Y-%m-%d'), adults_number, type_des, id, rooms_cnt)
        hotel_names = []
        prices = []
        for val in response['result']:
            hotel_names.append(val['hotel_name'])
            prices.append(val['composite_price_breakdown']['all_inclusive_amount']['value'])
        hotel_names, prices = zip(*sorted(zip(hotel_names, prices), key=lambda x: x[1]))
        hotel_cost = {
            'start_date': checkin_date.strftime('%Y-%m-%d'),
            'end_date': checkout_date.strftime('%Y-%m-%d'),
            'hotel_names': list(hotel_names),
            'prices': list(prices)
        }
        hotel_costs.append(hotel_cost)

        for cost in hotel_costs:
            start_date = cost['start_date']
            end_date = cost['end_date']
            hotel_names = cost['hotel_names']
            prices = cost['prices']
            df_temp = pd.DataFrame({
                'start_date': [start_date]*len(hotel_names),
                'end_date': [end_date]*len(hotel_names),
                'hotel_name': hotel_names,
                'price': prices
            })
            df_list.append(df_temp)

        df = pd.concat(df_list, ignore_index=True)
        df_sorted = df.sort_values(by='price', ascending=True).reset_index(drop=True)

    return df_sorted


def get_flight_data(type_val, origin_val, destination_val, adults_number, start_date, end_date):

    price_lst = []
    airline_lst = []

    url = "https://skyscanner44.p.rapidapi.com/search"

    querystring = {"adults":adults_number ,"origin": origin_val,"destination": destination_val ,"departureDate": start_date,"returnDate": end_date ,"currency":"USD"}
    headers = {
        "content-type": "application/octet-stream",
        "X-RapidAPI-Key": os.environ.get('RAPID_API_KEY'),
        "X-RapidAPI-Host": "skyscanner44.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring).json()



    if 'itineraries' not in response:
        return pd.DataFrame({'Airline': [], 'Price': [], 'Start Date': [start_date], 'End Date': [end_date]})

    if type_val == 'Best':
        type_val = 0

    elif type_val == 'Cheapest':
        type_val = 1

    elif type_val == 'Fastest':
        type_val = 2

    elif type_val == 'Direct':
        type_val = 3

    else:
        return 'Invalid type selected'

    if len(response['itineraries']['buckets']) == 0:
      return

    for val in (response['itineraries']['buckets'][type_val]['items']):
        price_lst.append(val['price']['formatted'])
        airline_lst.append(val['legs'][1]['segments'][0]['operatingCarrier']['name'])


    return pd.DataFrame({'Airline': airline_lst, 'Price': price_lst, 'Start Date': [start_date]* len(price_lst), 'End Date': [end_date] * len(price_lst)})


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


@app.post('/GetFinalCost')
async def get_final_cost(data: final_cost):

    # get hotel data
    start_date = data.start_date_val #str
    end_date = data.end_date_val #str
    num_days = data.num_days_val #int
    adults_number = data.adults_number_val #int
    num_rooms = data.num_rooms_val #str
    df_sorted  = calculate_hotel_costs(start_date, end_date, num_days, adults_number, data.type_des, data.des_id, num_rooms)

    # get flight data
    date_pairs = create_date_pairs(start_date, end_date, num_days)
    flight_data = pd.DataFrame()
    
    for pair in date_pairs:
        result = get_flight_data(data.type_val, data.origin_val, data.destination_val, str(data.adults_number_val), pair[0], pair[1])
        flight_data = pd.concat([flight_data, result], ignore_index=True)
        

    flight_data = flight_data.drop_duplicates()
    # convert price column to float type
    flight_data['Price'] = flight_data['Price'].str.replace('$', '').astype(float)

    # group by start and end dates and get the row with lowest price for each group
    flight_data = flight_data.sort_values('Price').groupby(['Start Date', 'End Date'], as_index=False).first()

    # reset index
    flight_data = flight_data.reset_index(drop=True)

    # output result as list of dictionaries
    result = flight_data.to_dict(orient='records')
    result = pd.DataFrame(result)

    merged_df = pd.merge(df_sorted, result, left_on='start_date', right_on = 'Start Date', how='inner')
    merged_df['Total_cost'] = merged_df['price'] + merged_df['Price']
    merged_df.sort_values(by = 'Total_cost')

    # get the lowest cost and if matches the budget, return the dataframe else return the first row with message stating that the budget is not enough but here is the best we can do
    if merged_df['Total_cost'].min() <= data.budget_val:
        # return merged_df.loc[merged_df['Total_cost'].idxmin()]
        response_data = {'data': merged_df.loc[merged_df['Total_cost'].idxmin()],
            'status_code': '200'}
    else:
        # print('The budget is not enough but here is the best we can do')
        # return merged_df.head(1)
        response_data = {'data': merged_df.head(1),
            'status_code': '200'}


    # response_data = {'data': df_sorted,
    #         'status_code': '200'}
    
    return response_data
    # return df_sorted
