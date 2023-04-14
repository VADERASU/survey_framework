from extract import data, utils

if __name__ == "__main__":
    parser = utils.build_parser()
    args = parser.parse_args()
    dir, img_dir = utils.check_args(args)

    raw_md = data.load_toml(dir)
    papers = data.load_bibtex(dir)
    images = data.load_images(dir, img_dir)

    # each section has children attribute only (maybe store icon file as well?)

    # each image has a reference to a Paper document, the path to the file and
    # a list of sections it belongs to
    # Paper will need a query to get all sections
    # associated with it from the images

    # figures out the children of all metadata nodes
    md = data.process_metadata(raw_md)
    # TODO: move into its own function, write tests
    for image, image_md in images.items():
        # map image to keywords
        for keyword, keyword_md in md.items():
            if image in keyword_md["images"]:
                image_md["keywords"].append(keyword)

    print(papers.entries)
    print(images)
    print(md)

    # TODO: import into MongoDB
