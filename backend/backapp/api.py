from ninja import NinjaAPI
import os

api = NinjaAPI()

@api.get("/health")
def healthchek(request):
    return {"status": "RUNNING"}




