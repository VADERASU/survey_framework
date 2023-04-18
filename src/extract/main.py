import sys

from pymongo import MongoClient, errors

from database.mongo import MongoWrapper
from extract import data, utils
from extract.tree import MetadataTree

if __name__ == "__main__":
    parser = utils.build_parser()
    args = parser.parse_args()
    dir, img_dir = utils.check_args(args)

    raw_md = data.load_toml(dir)
    papers = data.load_bibtex(dir)
    images = data.load_images(dir, img_dir)

    # build a tree for the metadata hierarchy
    md = MetadataTree(raw_md)
    data.map_image_keywords(images, md)

    client = MongoClient(serverSelectionTimeoutMS=2000)
    try:
        client.server_info()
    except errors.ServerSelectionTimeoutError as err:
        sys.exit(f"Error connecting to the database: {err}")

    db = MongoWrapper(client.surveys)
    db.populate(papers.entries_dict, md, images)
