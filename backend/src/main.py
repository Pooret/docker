from fastapi import FastAPI
import os

app = FastAPI()

API_KEY = os.environ.get("API_KEY")
MY_PROJECT = os.environ.get("PROJECT_NAME")

if not API_KEY:
    raise NotImplementedError("'API_KEY' was not set")

@app.get("/")
def read_index():
    return {"hello":"world again!", "project_name":MY_PROJECT, "API_KEY": API_KEY}

@app.get("/health")
def read_index():
    return {"status":"ok!"}