from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient, errors

import api.utils
from database.mongo import MongoWrapper
from database.utils import clean_mongo_result, list_to_dict

from .LaTexAccents import AccentConverter

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
    client = MongoClient(serverSelectionTimeoutMS=2000)
    try:
        client.server_info()
    except errors.ServerSelectionTimeoutError as err:
        raise HTTPException(
            status_code=500, detail=f"Error connecting to the database: {err}"
        )
    db = MongoWrapper(client.surveys)

    # TODO: move this to get_papers
    papers = list_to_dict(
        list(
            map(
                lambda e: clean_mongo_result(e),
                db.get_papers(survey),
            )
        ),
        "_id",
    )
    images = list(map(lambda e: clean_mongo_result(e), db.get_images(survey)))
    md = clean_mongo_result(db.get_metadata(survey))

    for image in images:
        # get image data as b64 strings
        data = api.utils.get_image_data(image["filename"])
        image["data"] = data
        # get keywords specific to this survey
        image["keywords"] = image["keywords"][survey]

    converter = AccentConverter()
    for paper, data in papers.items():
        # assume accents will be in authors field
        cleaned = converter.decode_Tex_Accents(data["author"], utf8_or_ascii=1)
        data["author"] = api.utils.drop_braces(cleaned)
        data["title"] = api.utils.drop_braces(
            api.utils.commands_to_utf8(data["title"])
        )
        papers[paper] = data

    return {"papers": papers, "images": images, "metadata": md}
