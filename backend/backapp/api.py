from ninja import NinjaAPI
import os
from .schema import ProfileSchema
from .models import EmberUser 
from django.shortcuts import get_object_or_404
api = NinjaAPI()

@api.get("/health")
def healthchek(request):
    return {"status": "RUNNING"}

#TODO: Subscriber code and write to db, chathistory endpoint, frontend websocket

@api.get("/profile", auth=CustomAuth(), response=ProfileSchema)
def profileview(request):
    phone= request.auth
    prof = get_object_or_404(EmberUser, phone=phone)
    return {"phone": prof.phone, "location": prof.location, "role": prof.role}




