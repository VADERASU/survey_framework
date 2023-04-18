import sys

from pymongo import MongoClient, errors

from database.mongo import MongoWrapper
from extract import data, utils
from extract.tree import MetadataTree


def main():
    parser = utils.build_parser()
    args = parser.parse_args()
    dir, img_dir = utils.check_args(args)

    client = MongoClient(serverSelectionTimeoutMS=2000)
    try:
        client.server_info()
    except errors.ServerSelectionTimeoutError as err:
        sys.exit(f"Error connecting to the database: {err}")

    survey_name = "survey"
    db = MongoWrapper(client.surveys)
    print(f"Update statistics for {survey_name}:\n")

    # TODO: test optional paper functionality
    papers = data.load_bibtex(dir)
    if papers is not None:
        p_up, p_in = db.add_papers(papers.entries_dict, survey_name)
        print(f"Updated {p_up} and inserted {p_in} papers.")

    # if metadata is updated, need to have images
    # if images are updated, only need to check that all keywords are valid
    raw_md = data.load_toml(dir)
    images = data.load_images(dir, img_dir)

    # build a tree for the metadata hierarchy
    md = MetadataTree(raw_md)
    data.map_image_keywords(images, md)

    # should be user-defined database to connect to
    db.populate(md, images, survey_name)


if __name__ == "__main__":
    main()
