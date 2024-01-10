import json
import os

from extract import data, utils
from extract.tree import MetadataTree

from .LaTexAccents import AccentConverter


def main():
    parser = utils.build_parser()
    args = parser.parse_args()
    dir, img_dir, icon_dir, data_dir, name = utils.check_args(args)

    # survey defaults to the name of the directory
    survey_name = os.path.basename(dir)
    if name is not None:
        survey_name = name

    # TODO: test optional paper functionality
    papers = data.load_bibtex(dir).entries_dict
    converter = AccentConverter()

    for paper, d in papers.items():
        # assume accents will be in authors field
        cleaned = converter.decode_Tex_Accents(d["author"], utf8_or_ascii=1)
        d["author"] = utils.drop_braces(cleaned)
        d["title"] = utils.drop_braces(utils.commands_to_utf8(d["title"]))
        papers[paper] = d

    images = data.load_images(dir, img_dir, set(papers.keys()))

    # only need images if any one image array changes - hard to test for though
    # if images are updated, only need to check that all keywords are valid
    raw_md = data.load_toml(dir)

    # build a tree for the metadata hierarchy
    md = MetadataTree(raw_md)
    data.map_image_keywords(images, md)
    data.load_icons(dir, icon_dir, md)

    md = md.to_dict()

    icons = {}

    def get_icon(children):
        for child in children:
            icons[child["name"]] = child["icon"]
            get_icon(child["children"])

    get_icon(md["children"])

    # need to return a json dict of the following
    j = json.dumps(
        {"papers": papers, "images": images, "metadata": md, "icons": icons}
    )

    with open(data_dir.joinpath(f"{survey_name}.json"), "w") as f:
        f.write(j)


if __name__ == "__main__":
    main()
