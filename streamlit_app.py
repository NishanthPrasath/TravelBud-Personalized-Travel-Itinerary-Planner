import streamlit as st
import requests
from backend import google_maps, top_10_places
from dotenv import load_dotenv
import os
import airportsdata
from datetime import datetime,timedelta
import pandas as pd

load_dotenv()

API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')

ACCESS_TOKEN = os.environ["access_token"]
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}


# Define background images
# home_bg = ""
# page_bg = ""

# Set page config
st.set_page_config(page_title="TravelBud", page_icon=":earth_americas:")

def get_top_attractions(destination, interests):
    
    data = {
        "city": destination,
        "types": interests
    }

    res = requests.post(
        'http://localhost:8000/GetTopAttractions', json=data)
    
    response = res.json()

    if response["status_code"] == 200 or response["status_code"] == '200':
        return response

def find_optimal_pairs(selected_places):

    data = {
            "locations": selected_places
        }

    res = requests.post(
        'http://localhost:8000/FindOptimalPairs', json=data)
                
    response = res.json()

    if response["status_code"] == 200 or response["status_code"] == '200':
        st.write(response["data"])

def get_location_id(destination):

    url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"

    querystring = {"name": destination,"locale":"en-gb"}

    headers = {
        "X-RapidAPI-Key": os.environ.get('RAPID_API_KEY'),
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    response = response.json()
    return response[1]['dest_id'], response[1]['dest_type']

def get_final_cost(start_date_val, end_date_val, num_days_val, adults_number_val, num_rooms_val, des_id, type_des, type_val, origin_val, destination_val, budget_val):

    data = {
        "start_date_val": start_date_val,
        "end_date_val": end_date_val,
        "num_days_val": num_days_val,
        "adults_number_val": adults_number_val,
        "num_rooms_val": num_rooms_val,
        "des_id": des_id,
        "type_des": type_des,
        "type_val": type_val,
        "origin_val": origin_val,
        "destination_val": destination_val,
        "budget_val": budget_val
    }

    res = requests.post(
        'http://localhost:8000/GetFinalCost', json=data)
    
    response = res.json()

    if response["status_code"] == 200 or response["status_code"] == '200':
        return response



# Helper function to format the selectbox options for places
def format_select_option(pair):
    return f"{pair[0]} ({pair[1]})"

def login():
    # Set background image
    # st.markdown(f'<style>body{{background-image: url({page_bg}); background-size: cover;}}</style>', unsafe_allow_html=True)

    st.subheader('Login')
    # Get user input
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        # Check if login is valid
        if email == "example@example.com" and password == "password":
            st.success("Logged in!")
        else:
            st.error("Incorrect email or password")

    if st.button("Forgot Password"):
        st.info("Enter your email address and we'll send you a link to reset your password")

        # Get user input
        email = st.text_input("Your Email")

        # Reset Password button
        if st.button("Reset Password"):
            # Check if email is valid
            if email == "example@example.com":
                st.success("Password reset link sent to email!")
            else:
                st.error("Email address not found")

def signup():
    # Set background image
    # st.markdown(f'<style>body{{background-image: url({page_bg}); background-size: cover;}}</style>', unsafe_allow_html=True)

    st.subheader('Signup')
    # Get user input
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    # Display a multiselect for the user to choose the place types
    selected_place_types = st.multiselect('Select your interests', google_maps.get_place_types())

    # Display the user's selection
    if selected_place_types:
        st.info("You selected: " + ", ".join(selected_place_types))

    # Join the selected types with the '|' separator
    types_str = '|'.join(selected_place_types)

    # Define the plans as a dictionary
    plans = {
        "Basic": "10",
        "Standard": "25",
        "Premium": "50"
    }

    # Create a radio button group to display the plans
    selected_plan = st.radio("Select a plan", list(plans.keys()))

    # Display the selected plan's details
    st.info(f"You have selected the {selected_plan} plan. With the {selected_plan} plan, you can make {plans[selected_plan]} requests")


    # Signup button
    if st.button("Create Account"):
        # Check if password matches
        if password != confirm_password:
            st.error("Passwords do not match")
        else:
            st.success("Signed up!")

def home_page():
    # Set background image
    # st.markdown(f'<style>body{{background-image: url({home_bg}); background-size: cover;}}</style>', unsafe_allow_html=True)
    st.markdown("# TravelBud")

    # Create a menu with the options
    menu = ["Select", "Login", "Signup"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Login":
        login()
    elif choice == "Signup":
        signup()


def plan_my_trip_page():
    # Set background image
    # st.markdown(f'<style>body{{background-image: url({page_bg}); background-size: cover;}}</style>', unsafe_allow_html=True)

    st.markdown("# TravelBud")
    st.subheader('Plan My Trip')
    # st.sidebar.markdown("# Page 2 ❄️")
    st.sidebar.button("Logout")

    # Loading airport data
    airports = airportsdata.load('IATA')

    # Extract city names and corresponding IATA codes
    city_iata_pairs = [(data['city'], code) for code, data in airports.items()]

    # Selectbox for city selection
    source = st.selectbox("Select a source city", options=["Select"]+[format_select_option(p) for p in city_iata_pairs])

    # if source != "Select":
    # Remove the selected source city from destination options
    destination_options = [format_select_option(p) for p in city_iata_pairs if p[0] != source.split(" (")[0]]
    destination = st.selectbox("Select a destination city", options=["Select"]+destination_options)

    # destination = st.selectbox("Select a destination city", options=[format_option(p) for p in city_iata_pairs])

    if source != "Select" and destination != "Select":
        # Extract the selected city and IATA code
        # city, iata = source.split(" (")
        source_iata = source.split(" (")[1][:-1]
        # city, iata = destination.split(" (")
        destination_iata = destination.split(" (")[1][:-1]    

        # st.write(f" {source_iata} and {destination_iata}")

    # User Inputs
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    num_days = st.number_input('Enter the number of days for your trip', min_value=1, max_value=365, step=1)
    num_people = st.number_input("Enter the number of people", value=1, min_value=1)

    # define default number of rooms
    num_rooms = 1

    if num_people > 1:
        num_rooms = st.number_input('Enter the number of rooms', value=1, min_value=1)

    type_val = st.radio("Select flight type",('Best', 'Cheapest', 'Fastest', 'Direct'))

    # Budget Slider
    budget = st.slider("Budget", min_value=0, max_value=10000, step=100)

    interests = 'tourist_attraction|amusement_park|park|point_of_interest|establishment'


    if destination != "Select":

        res = get_top_attractions(destination.split(" (")[0], interests)

        selected_places = st.multiselect('Select the places', res["data"])
        # Displaying the user's selection
        if selected_places:
            st.info("You selected: " + ", ".join(selected_places))


    if st.button("Submit"):

        st.write("Thank you for submitting your travel requirements!")

        with st.spinner('Processing'):
            find_optimal_pairs(selected_places)

            des_id, type_des= get_location_id(destination.split(" (")[0])

            res = get_final_cost(str(start_date), str(end_date), num_days, num_people, num_rooms, des_id, type_des, type_val, source_iata, destination_iata, budget)

            st.write(res["data"])


def my_account_page():
    # Set background image
    # st.markdown(f'<style>body{{background-image: url({page_bg}); background-size: cover;}}</style>', unsafe_allow_html=True)

    st.markdown("# TravelBud")
    st.subheader('My Account')
    # st.sidebar.markdown("# Page 3 🎉")
    st.sidebar.button("Logout")


    # Define the plans
    plans = {
        "Basic": "10",
        "Standard": "25",
        "Premium": "50"
    }

    # Create a radio button group to display the plans
    selected_plan = st.radio("Change your plan", list(plans.keys()))

    if selected_plan:
        # Display the selected plan's details
        st.info(f"You have selected the {selected_plan} plan. With the {selected_plan} plan, you can make {plans[selected_plan]} requests")
    
    
    # Display a multiselect for the user to choose the place types
    selected_place_types = st.multiselect('Update your interests', google_maps.get_place_types())

    # Display the user's selection
    if selected_place_types:
        st.info("You selected: " + ", ".join(selected_place_types))

    # Join the selected types with the '|' separator
    types_str = '|'.join(selected_place_types)

    st.button("Save")



def analytics_page():
    # Set background image
    # st.markdown(f'<style>body{{background-image: url({page_bg}); background-size: cover;}}</style>', unsafe_allow_html=True)

    st.markdown("# TravelBud")
    st.subheader('Dashboard')    
    # st.sidebar.markdown("# Page 3 🎉")
    st.sidebar.button("Logout")
    
    try:
        fastapi_url="http://fastapi:8000/get_useract_data"
        response=requests.get(fastapi_url,headers=headers)
    except:
        print('user activity data not yet generated') 
        
    def convert_to_date(date_string,format):
    
        date_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")
        
        if format=='date':
            return date_object.date().strftime('%Y-%m-%d')
        elif format=='hour':
            return date_object.hour
        elif format=='month':
            return date_object.month
        elif format=='week':
            return date_object.isocalendar()[1]

    def user_act_data(timeframe):
        
        if timeframe=="Hour":
            last_date = datetime.strptime(user_data['date'].iloc[-1], '%Y-%m-%d %H:%M:%S.%f')
            time_diff = datetime.utcnow() - last_date
            if time_diff <= timedelta(hours=1):
                api_hits=user_data['hit_count'].iloc[-1]
                rem_limit=user_data['api_limit'].iloc[-1]-api_hits
            else:
                api_hits=0
                rem_limit=user_data['api_limit'].iloc[-1]
                
        return api_hits,rem_limit

    def data_charts(timeframe):
        
        if timeframe=='Day':
            # print(user_data.columns)
            
            daily_count = user_data.groupby(['date_str','api_name'],as_index=False).agg({'date': 'count'})
            daily_count = daily_count.reset_index()
            daily_count = daily_count.rename(columns={'date': 'API Hits'})
            # print('y')
            return daily_count
        
        elif timeframe=='Week':
            week_count = user_data.groupby(['week','api_name']).agg({'date': 'count'})
            # reset index and rename columns
            week_count = week_count.reset_index()
            week_count = week_count.rename(columns={'date': 'API Hits'})
            return week_count
        
        elif timeframe=='Month':
            month_count = user_data.groupby(['month','api_name']).agg({'date': 'count'})
            # reset index and rename columns
            month_count = month_count.reset_index()
            month_count = month_count.rename(columns={'date': 'API Hits'})
            return month_count
        
    def make_chart(data,x_axis,y_axis,type,title):
        if type=='area':
            st.markdown(title)
            st.area_chart(
            data=data,
            x=x_axis,
            y=y_axis)
        elif type=='bar':
            st.markdown(title)
            st.bar_chart(
            data=data,
            x=x_axis,
            y=y_axis)

    try:
        if response.status_code==200:
            
            user_data_json=response.json()
            # print(user_data_json['data'])
            user_data = pd.DataFrame(user_data_json['data'])
            user_data['date_str']=user_data['date'].apply(convert_to_date,args=('date',))
            user_data['hour']=user_data['date'].apply(convert_to_date,args=('hour',))
            user_data['month']=user_data['date'].apply(convert_to_date,args=('month',)) 
            user_data['week']=user_data['date'].apply(convert_to_date,args=('week',)) 
            
        else:
            st.error("You haven't yet used our application")
            user_data=pd.DataFrame(columns=['username','service_plan','api_limit','date','api_name','hit_count','date_str','hour','month','week'])
        
        st.text('Your current plan - ' + str(user_data['service_plan'].iloc[-1]))


        api_hits=0
        rem_limit=0
        b1, b2 = st.columns(2)
        b1.metric("API HITs", user_act_data('Hour')[0])
        b2.metric("Remaining limit", user_act_data('Hour')[1])

        view_selection = st.radio("View by:",
                options=["Day", "Week", "Month"],
                horizontal=True
            )

        if view_selection=="Day":
            data=data_charts('Day')
            recent_date=data['date_str'].iloc[-1]
            recent_data=data[data['date_str']==recent_date]
            # print('000000')
            # print(recent_data)
            all_data = data.groupby(['date_str'],as_index=False).agg({'API Hits': 'sum'})
            all_data = all_data.reset_index()
            # all_data = all_data.rename(columns={'date': 'API Hits'})
            col1, col2 = st.columns(2)
            with col1:
                make_chart(recent_data,'api_name','API Hits','bar','### API Usage - Modules ')
            with col2:    
                make_chart(all_data,'date_str','API Hits','bar','### API Usage - Total')
        elif view_selection=="Week":
            data=data_charts('Week')
            recent_date=data['week'].iloc[-1]
            recent_data=data[data['week']==recent_date]
            make_chart(recent_data,'api_name','API Hits','bar','### API Usage - Modules ')
        elif view_selection=="Month":
            data=data_charts('Month')
            recent_date=data['month'].iloc[-1]
            recent_data=data[data['month']==recent_date]
            make_chart(recent_data,'api_name','API Hits','bar','### API Usage - Modules ')
            
    except:
        print('empty table error')



page_names_to_funcs = {
    "Home": home_page,
    "Account": my_account_page,
    "Plan My Trip": plan_my_trip_page,
    "Dashboard": analytics_page
}

selected_page = st.sidebar.radio("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
