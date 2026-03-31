from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/health")
def healthchek(request):
    return {"status": "RUNNING"}
