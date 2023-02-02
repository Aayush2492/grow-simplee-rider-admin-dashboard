from typing import Union

from fastapi import FastAPI, Request, HTTPException
import aiosql
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE = os.getenv('DATABASE')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASS = os.getenv('POSTGRES_PASS')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

conn = psycopg2.connect(
                    database=DATABASE, 
                    user=POSTGRES_USER, 
                    password=POSTGRES_PASS, 
                    host=POSTGRES_HOST, 
                    port=POSTGRES_PORT
)

print("Opened database successfully!")

app = FastAPI()
queries = aiosql.from_path("../db", "psycopg2")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/location")
async def add_locations(info : Request):
    details = await info.json()
    cur = conn.cursor()
    locations_to_add = details["locations"]
    # insert_query = "INSERT INTO location (latitude, longitude) VALUES (%s, %s)"
    for location in locations_to_add:
        # cur.execute(insert_query, (location["latitude"], location["longitude"],))
        queries.insert_location(
            conn,
            latitude=location["latitude"],
            longitude=location["longitude"]
        )

    try:
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=500, detail="Some Error Occured")