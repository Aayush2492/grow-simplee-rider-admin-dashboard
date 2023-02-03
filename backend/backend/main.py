from typing import Union, List

from fastapi import FastAPI, Request, HTTPException, status
import aiosql
import psycopg2
import os
from dotenv import load_dotenv
from models.models import Package, Location 

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
queries = aiosql.from_path("db", "psycopg2")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/location")
async def add_locations(locations: List[Location]):
    cur = conn.cursor()
    # insert_query = "INSERT INTO location (latitude, longitude) VALUES (%s, %s)"
    for loc in locations:
        # cur.execute(insert_query, (location["latitude"], location["longitude"],))
        queries.insert_location(
            conn,
            latitude=loc.latitude,
            longitude=loc.longitude
        )

    try:
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=500, detail="Some Error Occured")

@app.get('/package/{item_id}')
def get_item(item_id: int):

    return {"item":"item"}

@app.post('/package', status_code=status.HTTP_201_CREATED)
def add_item(package: Package):

    return {"message": "Item Created"}

@app.delete('/package/{item_id}')
def delete_item(item_id: int):

    return {"status":"ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
