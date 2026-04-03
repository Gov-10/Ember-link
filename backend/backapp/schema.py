from ninja import Schema
from typing import Optional
from datetime import datetime
class ProfileSchema(Schema):
   phone:str
   location:Optional[str]=None
   role:str

class ShelterSchema(Schema):
    name:str
    region:str
    latitude:float
    longitude:float
    total_capac:int
    occupied:int
    is_active:bool

class NgoSchema(Schema):
    org_name:str
    base_latitude:float
    base_longitude:float
    ambulances:int
    food_pac:int
    volunteers:int

class EmberSchema(Schema):
    role:str
    phone:str
    latitude:float
    longitude:float
    created_at:datetime

class FillSchema(Schema):
    org_name:str
    ambulances:int
    food_pac:int
    volunteers:int
