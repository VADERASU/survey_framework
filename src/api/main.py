import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient, errors

import api.utils
from database.mongo import MongoWrapper
from database.utils import clean_mongo_result, list_to_dict

from .LaTexAccents import AccentConverter

f = Path(__file__)
this_dir = f.parent

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_db/{survey}")
def get_db(survey: str):
    # for now, just test that the website works
    j = {}
    with open("2d_3d_combo.json") as f:
        j = json.load(f)
    return j


@app.get("/")
def frontend():
    return RedirectResponse(url="/index.html", status_code=303)


app.mount
