```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlite3 import Error
import sqlite3
import jwt
from typing import Optional

app = FastAPI()

# SQLite database connection
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('devops_pulse.db')
        return conn
    except Error as e:
        print(e)

# Create users table
def create_table():
    conn = create_connection()
    sql = """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            );"""
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

create_table()

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User model
class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

# Token model
class Token(BaseModel):
    access_token: str
    token_type: str

# Create a new user
@app.post("/users/")
async def create_user(user: User):
    conn = create_connection()
    sql = """INSERT INTO users(username, email, password) VALUES (?, ?, ?)"""
    try:
        c = conn.cursor()
        c.execute(sql, (user.username, user.email, user.password))
        conn.commit()
        return {"message": "User created successfully"}
    except Error as e:
        print(e)
        return {"message": "Error creating user"}

# Get a user by username
@app.get("/users/{username}")
async def get_user(username: str):
    conn = create_connection()
    sql = """SELECT * FROM users WHERE username = ?"""
    try:
        c = conn.cursor()
        c.execute(sql, (username,))
        user = c.fetchone()
        if user:
            return {"id": user[0], "username": user[1], "email": user[2]}
        else:
            return {"message": "User not found"}
    except Error as e:
        print(e)
        return {"message": "Error getting user"}

# Token endpoint
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = create_connection()
    sql = """SELECT * FROM users WHERE username = ?"""
    try:
        c = conn.cursor()
        c.execute(sql, (form_data.username,))
        user = c.fetchone()
        if user and user[3] == form_data.password:
            access_token_expires = 3600
            access_token = jwt.encode(
                {"sub": user[1], "exp": access_token_expires},
                "secret_key",
                algorithm="HS256"
            )
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Error as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Error logging in",
            headers={"WWW-Authenticate": "Bearer"},
        )
```