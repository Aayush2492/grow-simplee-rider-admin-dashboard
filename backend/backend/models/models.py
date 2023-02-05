from pydantic import BaseModel
from typing import Union
from datetime import datetime

class Package(BaseModel):
    weight: int
    length : int
    breadth: int
    height: int
    delivery_date: datetime
    delivery_loc: int
    erroneous : bool = False
    comments : Union[str, None] = None
    obj_type: bool = True
    completed: bool = False

class PackageOut(Package):
    object_id: int

class Location(BaseModel):
    latitude: float
    longitude: float
    address: str

class LocationOut(BaseModel):
    id: int

class Rider(BaseModel):
    longitude: float
    latitude: float
    current_trip : Union[int, None] = None

