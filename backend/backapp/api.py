from ninja import NinjaAPI
import os
from .schema import ProfileSchema, ShelterSchema, FillSchema
from .models import EmberUser,Shelter, NGOProfile
from typing import List
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from .auth import CustomAuth
api = NinjaAPI()

@api.get("/health")
def healthchek(request):
    return {"status": "RUNNING"}

#TODO:  chathistory endpoint

@api.post("/fill", auth=CustomAuth())
def fillNgo(request, payload:FillSchema):
    user=request.auth
    if user["role"] != "ngo":
        raise HttpError(403, "Not allowed to perform this action")
    org_name=payload.org_name
    ambulances=payload.ambulances
    food_pac=payload.food_pac
    volunteers=payload.volunteers
    latitude=user["latitude"]
    longitude=user["longitude"]
    NGOProfile.objects.create(user=user,org_name=org_name, ambulances=ambulances, food_pac=food_pac, volunteers=volunteers, base_latitude=latitude or 0, base_longitude=longitude or 0)
    return {"message": "added successfully"}

@api.get("/profile", auth=CustomAuth(), response=ProfileSchema)
def profileview(request):
    user= request.auth
    phone=user["phone"]
    prof = get_object_or_404(EmberUser, phone=phone)
    return {"phone": prof.phone, "location": prof.location, "role": prof.role}

@api.get("/shelters", response=List[ShelterSchema])
def list_shelters(request, region:str):
    shel= Shelter.objects.filter(region=region, is_active=True)
    return shel

@api.get("/ngos", response=List[NgoSchema])
def list_ngos(request):
    ngo=NGOProfile.objects.all()
    return ngo

@api.get("/users", response=List[EmberSchema])
def list_users(request, role:str):
    us=EmberUser.objects.filter(role=role)
    return us





