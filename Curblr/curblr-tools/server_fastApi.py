from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Body
from datetime import datetime, time
from fastapi.middleware.cors import CORSMiddleware
from run import *
from pydrive_logic import *
import json


app = FastAPI()

origins = [
    "*",
    "http://localhost"
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

'''
https://fastapi.tiangolo.com/tutorial/extra-data-types/
datetime.datetime:

A Python datetime.datetime.
In requests and responses will be represented as a str in ISO 8601 format, like: 2008-09-15T15:53:00+05:00.

'''

class Filter(BaseModel):
    true_date_time: Optional[datetime] 
    arrond_quartier:  Optional[str]  = "plaza" 
    price: Optional[float] = 0 
    maxStay: Optional[int] = 30
    minStay: Optional[int] = 30

@app.post("/items")
async def read_item(filter_params:Filter):
    print(filter_params.arrond_quartier)
    geojson = run([filter_params.arrond_quartier], filter_params.true_date_time, filter_params.price, filter_params.minStay)
    #UploadMapFile(geoson)
    return geojson#filter_params