import sys

from pymongo import MongoClient, errors

from database.mongo import MongoWrapper
from extract import data, utils
from extract.tree import MetadataTree


def main():
    parser = utils.build_parser()
    args = parser.parse_args()
    dir, img_dir, icon_dir = utils.check_args(args)

    client = MongoClient(serverSelectionTimeoutMS=2000)
    try:
        client.server_info()
    except errors.ServerSelectionTimeoutError as err:
        sys.exit(f"Error connecting to the database: {err}")

    # TODO: need to make sure this is no longer hardcoded
    survey_name = "2d_3d_combo"
    db = MongoWrapper(client.surveys)
    print(f"Update statistics for {survey_name}:\n")

    # TODO: test optional paper functionality
    papers = data.load_bibtex(dir)
    if papers is not None:
        p_up, p_in = db.add_papers(papers.entries_dict, survey_name)
        print(f"Updated {p_up} and inserted {p_in} papers.")

    ck = db.get_cite_key_to_id(survey_name)
    images = data.load_images(dir, img_dir, ck)

    # only need images if any one image array changes - hard to test for though
    # if images are updated, only need to check that all keywords are valid
    raw_md = data.load_toml(dir)

    # build a tree for the metadata hierarchy
    md = MetadataTree(raw_md)
    data.map_image_keywords(images, md)
    data.load_icons(dir, icon_dir, md)

    m_up, m_in = db.add_metadata(md, survey_name)
    if m_up:
        print("Metadata updated.")
    else:
        print("Metadata inserted." if m_in else "Metadata not modified.")

    i_up, i_in = db.add_images(images, survey_name)
    print(f"Updated {i_up} and inserted {i_in} images.")


if __name__ == "__main__":
    main()
