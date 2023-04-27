import schema
from fastapi import FastAPI,Depends
import os
import pandas as pd
from passlib.context import CryptContext
import access_token
from fastapi.security import OAuth2PasswordRequestForm
import common_utils as cu
import boto3
import DB_Connect as database

clientlogs = boto3.client('logs',
region_name= "us-east-1",
aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))

cwd = os.getcwd()
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()
db = database.DB()

@app.post('/login')
async def login(login_data: OAuth2PasswordRequestForm = Depends()):
    userTable = db.getTable('User_Details')
    user = pd.read_sql(db.selectWhere(userTable, 'UserID', login_data.username), db)
    if len(user) == 0:
        data = {"message": "User not found", "status_code": "404"}
    else:
        pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
        if pwd_cxt.verify(login_data.password, user['Password'][0]):
            print("password verified")
            data = {'message': 'Username verified successfully', 'status_code': '200'}
            accessToken = access_token.create_access_token(data={"sub": str(user['UserID'][0])})
            data = {'message': "Success",'access_token':accessToken,'service_plan': user['service_plan'][0],'status_code': '200'}
        else:
            data = {'message': 'Password is incorrect','status_code': '401'}
    return data

@app.post('/signup')
async def signup(user_data: schema.UserData):
    userTable = db.getTable('User_Details')
    user = pd.read_sql(db.selectWhere(userTable, 'UserID', user_data.Username), db)
    if len(user) == 0:
        pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_cxt.hash(user_data.Password)
        db.insertRow(userTable, [{'UserID': user_data.Username, 'Password': hashed_password, 'Name': user_data.Name, 'Plan': user_data.Plan}])
        data = {"message": "User created successfully", "status_code": "200"}
    else:
        data = {"message": "This email already exists", "status_code": "404"}
    return data