from fastapi import FastAPI
from pydantic import BaseModel
import validators
import sqlite3
import requests
from http import HTTPStatus
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env vars

BASE_URL = os.getenv("BASE_URL")
DB_PATH = os.getenv("DB_PATH")

# General db connection setup
connection = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = connection.cursor()


# Create table script
cursor.execute("CREATE TABLE IF NOT EXISTS URLSHORTNER(longurl TEXT, shorturl TEXT, code TEXT UNIQUE)")

app = FastAPI()


# Class structure creation using BaseModel for POST methods
class UrlRequest(BaseModel):
    url: str

# This funciton validates if the long url is valid
def validate_url_format(longurl: str):
    return validators.url(longurl)

# This function validates if the long url is a valid webaddress 
def validate_url(longurl: str):
    try:
        response = requests.get(longurl)
        print(response)
        if response.status_code == HTTPStatus.OK:
            return True
        return False
    
    except Exception as ex:
        print(ex)
        return False

# Shortern url algorithm
def shorten_url(longurl: str):
    import random
    import string

    chars = string.ascii_letters + string.digits
    domain = BASE_URL

    while True:
        code = "".join(random.choices(chars, k=6))
        existing = cursor.execute("SELECT code FROM URLSHORTNER WHERE code = ?", (code,)).fetchone()
        
        if not existing:
            break  # Unique code found, exit loop
    
    shorturl = domain+code

    try:
        cursor.execute("INSERT INTO URLSHORTNER VALUES (?, ?, ?)", (longurl, shorturl, code))
        connection.commit()

    except Exception as ex:
        print("DB Insert Error:", ex)

    return shorturl


# Routes
@app.get("/")
def root():
    return "Welcome to url-shortner api !!!"

@app.post("/shorten")
def shorten(request : UrlRequest):

    longurl = request.url
    print(longurl)

    try:
        if validate_url_format(longurl) and validate_url(longurl):
            shorturl = shorten_url(longurl)
        if not shorturl:
            raise ValueError("Invalid URL format or failed validation")
    except Exception as ex:
        return {"error": f"An error occurred: {str(ex)}"}
        # return {"error": "an error occured, try block didnt succeed, shoturl is not created"}
    
    return {"shorturl": shorturl}

@app.get("/{code}")
async def redirect_to_longurl(code: str):
    row = cursor.execute("SELECT LONGURL FROM URLSHORTNER WHERE CODE = ?", (code,)).fetchone()

    if row:
        longurl = row[0]
        return RedirectResponse(url=longurl)
    else:
        return HTTPStatus.NOT_FOUND

