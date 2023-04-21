import streamlit as st
import requests

# Define background images
# home_bg = ""
# page_bg = ""

# Set page config
st.set_page_config(page_title="TravelBud", page_icon=":earth_americas:")

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

def forgot_password():
    # Set background image
    # st.markdown(f'<style>body{{background-image: url({page_bg}); background-size: cover;}}</style>', unsafe_allow_html=True)

    st.subheader('Forgot Password')
    st.info("Enter your email address and we'll send you a link to reset your password")

    # Get user input
    email = st.text_input("Email")

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
    menu = ["Select", "Login", "Signup", "Forgot Password"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Login":
        login()
    elif choice == "Signup":
        signup()
    elif choice == "Forgot Password":
        forgot_password()

def plan_my_trip_page():
    # Set background image
    # st.markdown(f'<style>body{{background-image: url({page_bg}); background-size: cover;}}</style>', unsafe_allow_html=True)

    st.markdown("# TravelBud")
    st.subheader('Plan My Trip')
    # st.sidebar.markdown("# Page 2 ❄️")

    # destination = st.text_input("Enter your destination")

    # Available Destinations
    destination_list = ["Paris", "New York", "Tokyo", "London", "Rome"]
    destination = st.selectbox("Select your destination", destination_list)

    # User Inputs
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    # # Fetching Destinations from API
    # if destination:
    #     url = f"https://api.opentripmap.com/0.1/en/places/autocomplete?name={destination}&apikey=<YOUR_API_KEY>"
    #     response = requests.get(url)
    #     data = response.json()
    #     destination_list = [city["name"] for city in data]
    # else:
    #     destination_list = []

    # # Available Destinations
    # destination = st.selectbox("Select your destination", destination_list)

    # Budget Slider
    budget_min = 0
    budget_max = 1000
    flight_budget = st.slider("Flight Budget", min_value=budget_min, max_value=budget_max, step=100)
    hotel_budget = st.slider("Hotel Budget", min_value=budget_min, max_value=budget_max, step=100)

    # Interests Checkboxes
    st.write("Select your interests")
    interests = st.checkbox("Beaches")
    interests = st.checkbox("Museums")
    interests = st.checkbox("Historical Sites")
    interests = st.checkbox("National Parks")

    # Button to Submit
    if st.button("Submit"):
    # Do something with user inputs here, such as search for flights/hotels that match their criteria
        st.write("Thank you for submitting your travel requirements!")

def account():
    # Set background image
    # st.markdown(f'<style>body{{background-image: url({page_bg}); background-size: cover;}}</style>', unsafe_allow_html=True)

    st.markdown("# TravelBud")
    st.subheader('My Account')
    # st.sidebar.markdown("# Page 3 🎉")

def analytics():
    # Set background image
    # st.markdown(f'<style>body{{background-image: url({page_bg}); background-size: cover;}}</style>', unsafe_allow_html=True)

    st.markdown("# TravelBud")
    st.subheader('Dashboard')    
    # st.sidebar.markdown("# Page 3 🎉")

page_names_to_funcs = {
    "Home": home_page,
    "Account": account,
    "Plan My Trip": plan_my_trip_page,
    "Dashboard": analytics
}

selected_page = st.sidebar.radio("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
