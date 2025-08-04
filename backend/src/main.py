from fastapi import FastAPI
import os

app = FastAPI()

API_KEY = os.environ.get("API_KEY")
MY_PROJECT = os.environ.get("MY_PROJECT")

if not API_KEY:
    raise NotImplementedError("'API_KEY' was not set")

@app.get("/")
def read_index():
    return {"hello":"world again!", "project_name":MY_PROJECT}