from typing import Union, List
from pydantic import parse_obj_as
from fastapi import FastAPI, Request, HTTPException, status
import aiosql
import psycopg2
from psycopg2.extras import Json, RealDictCursor

import os
from dotenv import load_dotenv
from models.models import Package, Location, PackageOut
from fastapi.middleware.cors import CORSMiddleware
import json
# from routing.load import solve_routes

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

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/location")
async def add_locations(locations: List[Location]):
    cur = conn.cursor()
    ids = []
    try:
        for loc in locations:
            results = queries.insert_location(
                conn, latitude=loc.latitude, longitude=loc.longitude, address=loc.address)
            ids.append(results['loc_id'])
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=500, detail="Some Error Occured")
    return {'ids': ids}


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


@app.get("/solveall")
def solve_all():
    # First compute the distance matrix

    # Now solve the routes and get the trip locations
    # trips, trip_indices = solve_routes()
    # Now insert the trips to the DB, and assign the riders accordingly
    locations_order = "8.34234,48.23424;8.34423,48.26424;8.36424,48.29424"
    os.system(f"sh osrm.sh \"{locations_order}\"")
    input_file = open("result.json")
    result_data = json.load(input_file)
    with open("geo_jsons/geo_example.json") as f:
        geo_json = json.load(f)

    geo_json["features"][0]["geometry"] = result_data["routes"][0]["geometry"]
    tour_id = 1
    with open(f"geo_jsons/{tour_id}_geo.json", 'w') as f:
        json.dump(geo_json, f)
    return {"status": "ok"}


@app.post("/dynamic_pickup")
def pickup():
    """
    WIP
    """
    return {"status": "ok"}


@app.get("/riders")
def get_all_riders():
    """
    Get all the riders from the DB
    """
    try:
        results = queries.get_riders(conn)
    except Exception as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    return results

@app.get("/rider/{rider_id}")
def get_rider(rider_id: int):
    """
    Get the details of a particular rider from DB.
    """
    try:
        results = queries.get_rider_by_id(conn, rider_id=rider_id)
    except Exception as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    return results

@app.get("/rider/{rider_id}/viewtrip")
def viewroute(rider_id: int):
    """
    Will Give you a GeoJSON of a trip if the current trip exists. 
    Else, you get a status 404, indicating that you do not have a current trip
    """
    try:
        result = queries.check_trip(conn, rider_id=rider_id)
        if result['tour_status'] != None:
            with open("geo_jsons/{}_geo.json".format(result["tour_id"])) as f:
                geo_json = json.load(f)
            return {
                    "status": result['tour_status'],
                    "geo-json": geo_json
                    }

        if result is None:
            return {"status": -1}
            # raise HTTPException(
            #     status_code=404, detail='Trip not assigned or active')

    except Exception as err:
        conn.rollback()
        # raise HTTPException(status_code=500, detail=str(err))
        return {"status": -1}


@app.post("/rider/{rider_id}/accept")
def accept_trip(rider_id: int):
    try:
        results = queries.accept_trip(conn, rider_id=rider_id)
        conn.commit()
    except Exception as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    return {"status": results}


@app.post("/rider/{rider_id}/deliver/{object_id}")
def deliver_item(rider_id: int, object_id: int):
    """
    Marks Object ID as delivered.
    """
    try:
        results = queries.mark_delivered(conn, obj_id=object_id)
        trip_result = queries.check_trip(conn, rider_id=rider_id)
        trip_id = trip_result["tour_id"]
        count = queries.upcoming_deliveries(conn, tour_id=trip_id, object_id=object_id)
        
        if count[0]["count"] == 0:
            res = queries.complete_trip(conn, rider_id=rider_id)
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
        results = queries.check_trip(conn, rider_id=rider_id)
        # This query will return 0 if the current tour is accepted and 1 otherwise, 2 if no trip exists
        conn.commit()
    except Exception as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(err))

    return {"status": results}

@app.get("/trip/{object_id}")
def object_id_trip(object_id: int):
    """
    Returns the trip id in which the object will be delivered if it has been assigned a trip already
    Returns -1 if the object has not been assigned to any trip yet
    """
    try:
        results = queries.get_trip_id(conn, object_id=object_id)
    except Exception as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    if results != None:
        return {"trip": results["id"]}
    return {"trip": -1}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
