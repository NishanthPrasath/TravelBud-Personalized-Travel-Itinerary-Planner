# TravelBud

### Introduction

Travel Bud is an all-in-one vacation planning application designed to simplify the process of researching and booking flights, accommodations, and local attractions. The Personalized Travel Itinerary Planner creates tailored travel itineraries based on user preferences and budget constraints, making vacation planning a more efficient and enjoyable experience.

### Features

- Personalized recommendations based on user areas of interest
- Ability for users to update their password and preferences
- Rate limiting based on selected plans
- Appliction level analytics for detailed insights into application usage
- Top 10 list of locations based on the user's destination, along with **optimal pairing** between the locations
- Leveraging Booking.com API and Skyscanner API to help users find suitable accommodations and flights
- Assistance in creating an itinerary using the Chatgpt API and optimal prompting techniques
- Option to download itinerary in three languages (English, Spanish, and Hindi) delivered via Hugging Face models
- Coverage of a wide demographic, making it a global application

### Architecture Diagram


### Steps to reproduce
To run it locally please follow the steps below - 
- clone the repo 
- create a virtual environment and install requirements.txt
- subscribe to both these free tiers on Rapid API [Booking.com](https://rapidapi.com/tipsters/api/booking-com) and [Skyscanner.com](https://rapidapi.com/3b-data-3b-data-default/api/skyscanner44/)
- create a .env file with following variables
```
OPENAI_API_KEY=
AWS_ACCESS_KEY=
AWS_SECRET_KEY=
AWS_LOG_ACCESS_KEY = 
AWS_LOG_SECRET_KEY = 
bucket_name= <Enter AWS Bucket Name>
RAPID_API_KEY =
GOOGLE_MAPS_API_KEY = 
```


Attestation
WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK

Contribution:

- Dhanush Kumar Shankar: 25% 
- Nishanth Prasath: 25%
- Shubham Goyal: 25%
- Subhash Chandran Shankarakumar: 25%
