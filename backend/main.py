from backend import schema
from fastapi import FastAPI,Depends, APIRouter
import sqlite3
import os
import pandas as pd
from passlib.context import CryptContext
from backend import access_token
from backend import oauth2
from fastapi.security import OAuth2PasswordRequestForm
import boto3

clientlogs = boto3.client('logs',
region_name= "us-east-1",
aws_access_key_id=os.environ.get('AWS_LOG_ACCESS_KEY'),
aws_secret_access_key=os.environ.get('AWS_LOG_SECRET_KEY'))

cwd = os.getcwd()
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

@app.post('/login')
async def read_root(login_data: OAuth2PasswordRequestForm = Depends()):
    # try:
    database_file_name = "travel_app.db"
    database_file_path = os.path.join(project_dir, os.path.join('backend/',database_file_name))
    db = sqlite3.connect(database_file_path)
    user= pd.read_sql_query('SELECT * FROM Users where username="{}"'.format(login_data.username), db)
    if len(user) == 0:
        data = {"message": "User not found", "status_code": "404"}
    else:
        pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
        if pwd_cxt.verify(login_data.password, user['hashed_password'][0]):
            print("password verified")
            data = {'message': 'Username verified successfully', 'status_code': '200'}
            accessToken = access_token.create_access_token(data={"sub": str(user['username'][0])})
            data = {'message': "Success",'access_token':accessToken,'service_plan': user['service_plan'][0],'status_code': '200'}
        else:
            data = {'message': 'Password is incorrect','status_code': '401'}
    # except Exception as e:
    #     data = {'message': str(e),'status_code': '500'}
    return data