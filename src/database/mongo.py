"""
Wrapper around a pymongo.Database object to populate the database with the data
from the extraction script. Will add support for querying the database.
"""

from datetime import datetime
from typing import Any, Dict

from pymongo.database import Database

from extract import data
from extract.data import Image, MetadataDict


class MongoWrapper(Database):
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
        """
        Adds papers from a dictionary. The keys will become
        the cite_key field in the database.

        :param papers: A regular dictionary.
        """
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

    def populate(
        self,
        papers: Dict[str, Any],
        md: MetadataDict,
        images: Dict[str, Image],
        survey_name: str = "survey",
    ):
        """
        Populates the database.

        :param papers: Papers dictionary to insert.
        :param md: Metadata dictionary to insert.
        :param images: Image dictionary to insert.
        :param survey_name: Name of the survey to insert.
        """
        self.add_papers(papers)
        self.add_metadata(md, survey_name)
        self.add_images(images)

    def add_metadata(self, metadata: MetadataDict, survey_name: str):
        """
        Adds a metadata dictionary to the database.

        :param metadata: Metadata dictionary to insert.
        :param survey_name: Name of the survey it will relate to.
        """
        document = data.build_hierarchy(metadata)
        self.metadata.update_one(
            {"survey": survey_name},
            {"$set": {"hierarchy": document, "survey": survey_name}},
            upsert=True,
        )

    def get_metadata_hierarchy(self, survey_name: str = "survey"):
        """
        Gets the metadata hierarchy.
        """
        return self.metadata.aggregate(
            [{"$match": survey_name}, {"$unwind": "$hierarchy"}]
        )

    def add_images(self, images: Dict[str, Image]):
        """
        Adds images to database.

        :param images: Dictionary of strings to Images.
        """
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
