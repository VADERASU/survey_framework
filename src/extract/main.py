from pymongo import MongoClient

from database.mongo import MongoWrapper
from extract import data, utils

if __name__ == "__main__":
    parser = utils.build_parser()
    args = parser.parse_args()
    dir, img_dir = utils.check_args(args)

    raw_md = data.load_toml(dir)
    papers = data.load_bibtex(dir)
    images = data.load_images(dir, img_dir)
    # figures out the children of all metadata nodes
    md = data.process_metadata(raw_md)

    # TODO: move into its own function, write tests
    for image, image_md in images.items():
        # map image to keywords
        for keyword, keyword_md in md.items():
            if image in keyword_md["images"]:
                image_md["keywords"].append(keyword)

    client = MongoClient()
    db = MongoWrapper(client.surveys)
    db.populate(papers.entries_dict, md, images)
