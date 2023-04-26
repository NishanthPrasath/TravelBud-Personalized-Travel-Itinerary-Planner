from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, TEXT, Identity, inspect, select, update,insert
from sqlalchemy_utils import database_exists, create_database
import pandas as pd

config={'DB_USER_NAME':'postgres',
        'DB_PASSWORD':'shubh',
        'DB_ADDRESS':'localhost',
        'DB_NAME':'final_project'}

engine=create_engine('postgresql://'+str(config.get('DB_USER_NAME'))+':'+str(config.get('DB_PASSWORD'))+'@'+str(config.get('DB_ADDRESS'))+':5432/'+str(config.get('DB_NAME')))

connection = engine.connect()
metadata = MetaData()
user_data = Table('user_data', metadata, autoload_with=engine)

# Print the column names
print(user_data.columns.keys())

# Print full table metadata
print(repr(metadata.tables['user_data']))

query = insert(user_data) 
values_list = [{'UserID':'dhanush@gmail.com', 'Password':'abcd', 'AOI':'tourist attraction, hiking', 'Name':'Dhanush', 'Plan':'Basic'},
               {'UserID':'nishant@gmail.com', 'Password':'abcd', 'AOI':'tourist attraction, hiking, food', 'Name':'Nishant', 'Plan':'Standard'},
               {'UserID':'shubham@gmail.com', 'Password':'abcd', 'AOI':'tourist attraction, hiking, museums', 'Name':'Shubham', 'Plan':'Premium'}
               ]

ResultProxy = connection.execute(query,values_list)
query=select(user_data.c.UserID,user_data.c.Password,user_data.c.AOI,user_data.c.Name,user_data.c.Plan)
results = connection.execute(query).fetchall()
connection.commit()
print(results)

user_activity = Table('user_activity', metadata, autoload_with=engine)

# Print the column names
print(user_activity.columns.keys())

# # Print full table metadata
print(repr(metadata.tables['user_activity']))

query = insert(user_activity) 
values_list = [{'UserID':'dhanush@gmail.com', 'Source':'Boston', 'Destination':'New York', 'S_Date':'2023/05/01', 'E_Date':'2023/05/15', 'Duration':'5', 'Budget':'2500' , 'TotalPeople':'4', 'PlacesToVisit': 'Edge,Central Park, xyz','time_stamp':'2023/04/26'},
               {'UserID':'nishant@gmail.com', 'Source':'Boston', 'Destination':'New York', 'S_Date':'2023/05/01', 'E_Date':'2023/05/15', 'Duration':'5', 'Budget':'2500' , 'TotalPeople':'4', 'PlacesToVisit': 'Edge,Central Park, xyz','time_stamp':'2023/04/26'},
               {'UserID':'shubham@gmail.com', 'Source':'Boston', 'Destination':'San francisco', 'S_Date':'2023/05/05', 'E_Date':'2023/05/15', 'Duration':'10', 'Budget':'3500' , 'TotalPeople':'2', 'PlacesToVisit': 'Golden Gate Bridge,xyz','time_stamp':'2023/04/26'},
               {'UserID':'dhanush@gmail.com', 'Source':'New york', 'Destination':'Boston', 'S_Date':'2023/06/01', 'E_Date':'2023/06/15', 'Duration':'5', 'Budget':'2500' , 'TotalPeople':'4', 'PlacesToVisit': 'Boston Commons, Northeastern University, seaport','time_stamp':'2023/04/26'},
               ]

ResultProxy = connection.execute(query,values_list)
query=select(user_activity.c.UserID,user_activity.c.Source,user_activity.c.Destination,user_activity.c.S_Date,user_activity.c.E_Date,user_activity.c.Duration,user_activity.c.Budget,user_activity.c.TotalPeople,user_activity.c.PlacesToVisit,user_activity.c.time_stamp)
results = connection.execute(query).fetchall()
connection.commit()
print(results)


@app.get("/get_useract_data")
async def useract_data(getCurrentUser: schema.TokenData = Depends(oauth2.get_current_user)):
    config={'DB_USER_NAME':'postgres',
        'DB_PASSWORD':'shubh',
        'DB_ADDRESS':'localhost',
        'DB_NAME':'final_project'}
    engine=create_engine('postgresql://'+str(config.get('DB_USER_NAME'))+':'+str(config.get('DB_PASSWORD'))+'@'+str(config.get('DB_ADDRESS'))+':5432/'+str(config.get('DB_NAME')))
    connection = engine.connect()
    metadata = MetaData()
    try:
        user_data = Table('user_data', metadata, autoload_with=engine)
        query=select(user_data.c.UserID,user_data.c.Password,user_data.c.AOI,user_data.c.Name,user_data.c.Plan)
        results = connection.execute(query).fetchall()
        user_data=pd.DataFrame(results,columns=['UserID','Password','AOI','Name','Plan'])
        df_user_data=user_data.to_dict(orient='records')
        user_activity = Table('user_activity', metadata, autoload_with=engine)
        query=select(user_activity.c.UserID,user_activity.c.Source,user_activity.c.Destination,user_activity.c.S_Date,user_activity.c.E_Date,user_activity.c.Duration,user_activity.c.Budget,user_activity.c.TotalPeople,user_activity.c.PlacesToVisit,user_activity.c.time_stamp)
        results = connection.execute(query).fetchall()
        user_activity=pd.DataFrame(results,columns=['UserID','Source','Destination','S_Date','E_Date','Duration','Budget','TotalPeople','PlacesToVisit','time_stamp'])
        df_user_activity=user_activity.to_dict(orient='records')
        return {'user_data':df_user_data,'user_activity':df_user_activity}
    except:
        return {'data':'No data found'}
    
@app.post("/get_current_username")
async def get_username(getCurrentUser: schema.TokenData = Depends(oauth2.get_current_user)):
    
    # print(getCurrentUser)
    
    return {'username': getCurrentUser.username}