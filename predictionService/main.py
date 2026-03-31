from fastapi import FastAPI
app = FastAPI()
@app.get("/health")
def healthchek():
    return {"status": "RUNNING"}
