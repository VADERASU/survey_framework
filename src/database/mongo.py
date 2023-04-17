from datetime import datetime
from typing import Any, Dict

from bson import ObjectId
from pymongo.database import Database

from extract import data


class MongoWrapper(Database):
    cite_key_to_id: Dict[str, ObjectId]

    def __init__(self, database):
        self.database = database
        self.database.papers.create_index("cite_key")
        self.database.metadata.create_index("survey")
        self.database.images.create_index("filename")

    def __getattr__(self, attr):
        return getattr(self.database, attr)

    def __get_cite_key_to_id(self):
        collection = self.database.papers.find({})
        cite_key_to_id = {}
        for paper in collection:
            object_id = paper["_id"]
            cite_key = paper["cite_key"]
            cite_key_to_id[cite_key] = object_id
        return cite_key_to_id

    def add_papers(self, papers: Dict[str, Any]):
        for cite_key, paper_data in papers.items():
            self.papers.update_one(
                {"cite_key": cite_key},
                {
                    "$set": {
                        **paper_data,
                        "cite_key": cite_key,
                        "last_modified": datetime.utcnow(),
                    }
                },
                upsert=True,
            )

    def populate(self, papers, md, images):
        self.add_papers(papers)
        self.add_metadata(md)
        self.add_images(images)

    def add_metadata(self, metadata):
        document = data.build_hierarchy(metadata)
        # TODO: allow naming of survey
        # db.metadata.aggregate([{$unwind: '$hierarchy'}])
        self.metadata.update_one(
            {"survey": "survey"},
            {"$set": {"hierarchy": document, "survey": "survey"}},
            upsert=True,
        )

    def add_images(self, images):
        cite_keys = self.__get_cite_key_to_id()
        for filename, image in images.items():
            paper_ref = cite_keys[image["paper"]]
            keywords = image["keywords"]
            self.images.update_one(
                {"filename": filename},
                {
                    "$set": {
                        "filename": filename,
                        "keywords": keywords,
                        "paper": paper_ref,
                    }
                },
                upsert=True,
            )
