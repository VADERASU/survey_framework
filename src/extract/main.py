from extract import metadata, utils

if __name__ == "__main__":
    parser = utils.build_parser()
    args = parser.parse_args()
    dir = utils.check_args(args)

    raw_md = utils.load_toml(dir)
    papers = utils.load_bibtex(dir)
    images = utils.load_images(dir)

    # now we have the taxonomy, a list of papers, and the images
    # set up the database

    # each section has children attribute only (maybe store icon file as well?)

    # each image has a reference to a Paper document, the path to the file and
    # a list of sections it belongs to
    # Paper will need a query to get all sections
    # associated with it from the images

    # figures out the children of all metadata nodes
    md = {}
    for section in raw_md.keys():
        s = metadata.process_section(
            section, raw_md[section]
        )  # header sections
        md.update(**s)

    for image, image_md in images.items():
        # map image to keywords
        for keyword, keyword_md in md.items():
            if image in keyword_md["images"]:
                image_md["keywords"].append(keyword)
