"""
Wrapper around a pymongo.Database object to populate the database with the data
from the extraction script. Will add support for querying the database.
"""

from typing import Any, Dict, List

from pymongo.database import Database
from pymongo.results import UpdateResult
from typeguard import typechecked

from extract.data import Image
from extract.tree import MetadataTree


# TODO: add more queries?
class MongoWrapper(Database):
    def __init__(self, database):
        self.database = database
        self.database.papers.create_index("cite_key")
        self.database.metadata.create_index("survey")
        self.database.images.create_index("filename")

    # breaks with typechecking
    def __getattr__(self, attr):
        return getattr(self.database, attr)

    def __get_cite_key_to_id(self):
        """
        Gets a mapping of object IDs to paper titles.
        """
        collection = self.database.papers.find({})
        cite_key_to_id = {}
        for paper in collection:
            object_id = paper["_id"]
            cite_key = paper["cite_key"]
            cite_key_to_id[cite_key] = object_id
        return cite_key_to_id

    @typechecked
    def add_papers(self, papers: Dict[str, Any]):
        """
        Adds papers from a dictionary. The keys will become
        the cite_key field in the database.

        :param papers: A regular dictionary.
        """
        results = []
        for cite_key, paper_data in papers.items():
            r = self.papers.update_one(
                {"cite_key": cite_key},
                {
                    "$set": {
                        **paper_data,
                        "cite_key": cite_key,
                        # "last_modified": datetime.utcnow(),
                    }
                },
                upsert=True,
            )
            results.append(r)
        return self.__count_results(results)

    @typechecked
    def populate(
        self,
        papers: Dict[str, Any],
        md: MetadataTree,
        images: Dict[str, Image],
        survey_name: str = "survey",
        print_statistics: bool = True,
    ):
        """
        Populates the database.

        :param papers: Papers dictionary to insert.
        :param md: Metadata dictionary to insert.
        :param images: Image dictionary to insert.
        :param survey_name: Name of the survey to insert.
        :param print_statistics: Whether or not to print statistics.
        Default true.
        """
        p_up, p_in = self.add_papers(papers)
        m_up, m_in = self.add_metadata(md, survey_name)
        i_up, i_in = self.add_images(images)

        if print_statistics:
            print(f"Update statistics for {survey_name}:\n")
            print(f"Updated {p_up} and inserted {p_in} papers.")
            print(f"Updated {i_up} and inserted {i_in} images.")
            if m_up:
                print("Metadata updated.")
            else:
                print(
                    "Metadata inserted" if m_in else "Metadata not modified."
                )

    @typechecked
    def add_metadata(self, metadata: MetadataTree, survey_name: str):
        """
        Adds a metadata dictionary to the database.

        :param metadata: Metadata dictionary to insert.
        :param survey_name: Name of the survey it will relate to.

        :returns: Int (0 or 1) if the metadata was updated (0) or inserted (1).
        """

        r = self.metadata.update_one(
            {"survey": survey_name},
            {
                "$set": {
                    "hierarchy": metadata.to_dict(),
                    "survey": survey_name,
                }
            },
            upsert=True,
        )

        return self.__count_results([r])

    @typechecked
    def get_metadata_hierarchy(self, survey_name: str = "survey"):
        """
        Gets the metadata hierarchy for the specified survey.

        :param: The name of the survey.
        """
        return self.metadata.find_one({"survey": survey_name})["hierarchy"]

    @typechecked
    def __count_results(self, results: List[UpdateResult]):
        updated = 0
        inserted = 0
        for r in results:
            if r.matched_count:
                if r.modified_count:
                    updated += 1
            else:
                inserted += 1
        return updated, inserted

    @typechecked
    def add_images(self, images: Dict[str, Image]):
        """
        Adds images to database. Returns how many were updated or
        inserted.

        :param images: Dictionary of strings to Images.
        """
        cite_keys = self.__get_cite_key_to_id()
        results = []
        for filename, image in images.items():
            paper_ref = cite_keys[image["paper"]]
            keywords = image["keywords"]
            r = self.images.update_one(
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
            results.append(r)

        return self.__count_results(results)
