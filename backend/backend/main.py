from typing import Union, List

from pydantic import parse_obj_as
from fastapi import FastAPI, Request, HTTPException, status
import aiosql
import psycopg2
from psycopg2.extras import Json, RealDictCursor

import os
from dotenv import load_dotenv
from models.models import Package, Location, PackageOut

load_dotenv()

DATABASE = os.getenv("DATABASE")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASS = os.getenv("POSTGRES_PASS")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

conn = psycopg2.connect(
    database=DATABASE,
    user=POSTGRES_USER,
    password=POSTGRES_PASS,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    cursor_factory=RealDictCursor,
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
        queries.insert_location(conn, latitude=loc.latitude, longitude=loc.longitude)

    try:
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=500, detail="Some Error Occured")


@app.get("/packages", response_model=List[PackageOut])
def get_all_packages():
    """
    Get the List of All Packages present in the DB
    """
    try:
        results = queries.get_all_packages(conn)
    except Exception as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    return parse_obj_as(List[PackageOut], results)


@app.get("/package/{obj_id}", response_model=PackageOut)
def get_package(obj_id: int):
    """
    Get the details of a particular package from DB.
    """
    try:
        results = queries.get_package_by_id(conn, obj_id=obj_id)
    except Exception as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    return PackageOut.parse_obj(results)


@app.post("/package", status_code=status.HTTP_201_CREATED)
def add_package(item: Package):
    """
    Adds a Package with the given parameters in the database.
    """
    try:
        results = queries.insert_package(conn, **dict(item))
        conn.commit()
    except Exception as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=err)
    return {"message": results}


@app.patch("/package/{obj_id}")
def edit_package(obj_id: int):

    return {"message": "ok"}


@app.delete("/package/{obj_id}")
def delete_package(obj_id: int):
    """
    Delete Objects whose object_id is equal to the passed id.
    """
    try:
        results = queries.delete_package(conn, obj_id=obj_id)
        conn.commit()
    except Exception as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(err))

    return {"num_deleted": results}


@app.post("/solveall")
def solve_all():
    return {"status": "ok"}


@app.post("/dynamic_pickup")
def pickup():
    """
    WIP
    """
    pass
    return {"status": "ok"}


@app.post("/rider/{rider_id}/accept")
def accept_trip(rider_id: int):
    try:
        results = queries.accept_trip(conn, rider_id=rider_id)
        conn.commit()
    except Exception as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    return {"status": results}


@app.post("/rider/{rider_id}/deliver")
def deliver_item(rider_id: int, object_id: int):
    """
    Marks Object ID as delivered.
    """
    try:
        results = queries.mark_delivered(conn, rider_id=rider_id, obj_id=object_id)
        conn.commit()
    except Exception as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    return {"status": "ok"}


@app.post("/rider/{rider_id}/track")
def update_loc(rider_id: int, latitude: float, longitude: float):
    """
    Update the location of a rider, with his current latitude and longitude
    Status Code: 1 if tour accepted, 0 if tour not accepted
    """
    try:
        results = queries.update_loc(
            conn, rider_id=rider_id, latitude=latitude, longitude=longitude
        )
        # This query will return 0 if the current tour is accepted and 1 otherwise, 2 if no trip exists
        conn.commit()
    except Exception as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(err))

    return {"status": results}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
