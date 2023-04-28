from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, TEXT, Identity, inspect, select, update,insert
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
from datetime import datetime

config={'DB_USER_NAME':'postgres',
        'DB_PASSWORD':'postgres',
        'DB_ADDRESS':'database-1.ctwoomj0yrue.us-east-2.rds.amazonaws.com',
        'DB_NAME':'postgres'}

engine=create_engine('postgresql://'+str(config.get('DB_USER_NAME'))+':'+str(config.get('DB_PASSWORD'))+'@'+str(config.get('DB_ADDRESS'))+':5432/'+str(config.get('DB_NAME')))

connection = engine.connect()
metadata = MetaData()
user_data = Table('User_Details', metadata, autoload_with=engine)

# Print the column names
print(user_data.columns.keys())

# Print full table metadata
print(repr(metadata.tables['User_Details']))

query = insert(user_data) 
values_list = [{'UserID':'dhanush@gmail.com', 'Password':'abcd', 'Name':'Dhanush', 'Plan':'Basic', 'Hit_count_left':10},
               {'UserID':'nishant@gmail.com', 'Password':'abcd', 'Name':'Nishant', 'Plan':'Standard', 'Hit_count_left':25},
               {'UserID':'shubham@gmail.com', 'Password':'abcd', 'Name':'Shubham', 'Plan':'Premium', 'Hit_count_left':50}
               ]

ResultProxy = connection.execute(query,values_list)
query=select(user_data.c.UserID,user_data.c.Password,user_data.c.Name,user_data.c.Plan)
results = connection.execute(query).fetchall()
print(results)

User_Activity = Table('User_Activity', metadata, autoload_with=engine)

# Print the column names
print(User_Activity.columns.keys())

# # Print full table metadata
print(repr(metadata.tables['User_Activity']))

query = insert(User_Activity) 
values_list = [{'UserID':'dhanush@gmail.com', 'Source':'Boston', 'Destination':'New York', 'S_Date':'2023/05/01', 'E_Date':'2023/05/15', 'Duration':'5', 'Budget':'2500' , 'TotalPeople':'4','Time_stamp':datetime.utcnow()},
               {'UserID':'nishant@gmail.com', 'Source':'Boston', 'Destination':'New York', 'S_Date':'2023/05/01', 'E_Date':'2023/05/15', 'Duration':'5', 'Budget':'2500' , 'TotalPeople':'4','Time_stamp':datetime.utcnow()},
               {'UserID':'shubham@gmail.com', 'Source':'Boston', 'Destination':'San francisco', 'S_Date':'2023/05/05', 'E_Date':'2023/05/15', 'Duration':'10', 'Budget':'3500' , 'TotalPeople':'2','Time_stamp':datetime.utcnow()},
               {'UserID':'dhanush@gmail.com', 'Source':'New york', 'Destination':'Boston', 'S_Date':'2023/06/01', 'E_Date':'2023/06/15', 'Duration':'5', 'Budget':'2500' , 'TotalPeople':'4','Time_stamp':datetime.utcnow()},
               ]

ResultProxy = connection.execute(query,values_list)
query=select(User_Activity.c.UserID,User_Activity.c.Source,User_Activity.c.Destination,User_Activity.c.S_Date,User_Activity.c.E_Date,User_Activity.c.Duration,User_Activity.c.Budget,User_Activity.c.TotalPeople,User_Activity.c.Time_stamp)
results = connection.execute(query).fetchall()
print(results)


plan = Table('plan', metadata, autoload_with=engine)

# Print the column names
print(plan.columns.keys())

# # Print full table metadata
print(repr(metadata.tables['plan']))

query = insert(plan) 
values_list = [{'plan_name':'Basic', 'api_limit':10},
               {'plan_name':'Standard', 'api_limit':25},
               {'plan_name':'Premium', 'api_limit':50}
               ]

ResultProxy = connection.execute(query,values_list)
query=select(plan.c.plan_name,plan.c.api_limit)
results = connection.execute(query).fetchall()
print(results)


aoi = Table('AOI', metadata, autoload_with=engine)

# Print the column names
print(aoi.columns.keys())

# # Print full table metadata
print(repr(metadata.tables['AOI']))

query = insert(aoi) 
values_list = [{'UserID':'dhanush@gmail.com', 'Interest':'tourist attraction, hiking'},
               {'UserID':'nishant@gmail.com', 'Interest':'tourist attraction, hiking, food'},
               {'UserID':'shubham@gmail.com', 'Interest':'tourist attraction, hiking, museums'}
               ]

ResultProxy = connection.execute(query,values_list)
query=select(aoi.c.UserID,aoi.c.Interest)
results = connection.execute(query).fetchall()
print(results)