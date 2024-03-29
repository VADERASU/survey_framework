import os
import shutil
from pathlib import Path
from typing import Dict, List, TypedDict

import bibtexparser
import toml
from bson import ObjectId
from typeguard import typechecked

from extract import utils
from extract.tree import MetadataTree


# TODO: validate metadata here? or let tree do it?
@typechecked
def load_toml(directory: Path):
    p = utils.join_file(directory, "metadata.toml")
    return toml.load(p)


# TODO: validate?
@typechecked
def load_bibtex(directory: Path):
    data = None
    try:
        p = utils.join_file(directory, "papers.bib")
        with open(p) as bib_tex:
            data = bibtexparser.load(bib_tex)
    except FileNotFoundError:
        print("papers.bib not found. Looking for papers in database.")

    return data


class Image(TypedDict):
    keywords: List[str]
    paper: ObjectId


# TODO: test image-paper validation
@typechecked
def load_images(
    directory: Path, destination: Path, valid_papers: Dict[str, ObjectId]
) -> Dict[str, Image]:
    """
    Loads images from {directory} and copies them to {destination}.

    :param directory: Path to directory to load images from.
    :param destination: Path to copy images to.
    :return: A dictionary of strings to Image objects.
    :raises ValueError: Raised if the directory did not contain
    any image files.
    """
    p = utils.join_directory(directory, "images")
    img_types = ("jpg", "jpeg", "png", "gif")
    extracted = {}
    for img_type in img_types:
        images = list(p.glob(f"**/*.{img_type}"))
        for image in images:
            # in case someone names a directory like image.png/
            if image.is_file():
                shutil.copy2(image, destination)
                f_name = os.path.basename(image)
                paper = utils.extract_paper_from_image(f_name)
                if paper not in valid_papers.keys():
                    raise ValueError(
                        f"Paper {paper} does not exist in database."
                    )

                extracted[f_name] = {
                    "keywords": [],
                    "paper": valid_papers[paper],
                }

    if len(extracted.values()) == 0:
        raise ValueError(
            f"{p} does not contain any of the supported\
            image types {img_types}."
        )

    return extracted


# TODO: make method of MetadataTree, test
def map_image_keywords(images: Dict[str, Image], md: MetadataTree):
    """
    Maps images to their keywords using a Metadata tree.

    :param images: Dictionary of image file names to data.
    :param md: MetadataTree; see tree.py
    """
    # remove root
    nodes = list(filter(lambda n: n.tag != "root", md.all_nodes()))
    for image, image_md in images.items():
        for keyword in nodes:
            kw_images = md.get_keyword_images(keyword.tag)
            if image in kw_images:
                image_md["keywords"].append(keyword.tag)

    # find any images that are missing keywords
    missing = list(
        filter(lambda k: len(images[k]["keywords"]) == 0, images.keys())
    )

    if len(missing) > 0:
        raise ValueError(f"Images missing keywords: {missing}.")


# TODO: typecheck
def load_icons(directory, destination, md):
    """
    [TODO:description]

    :param directory [TODO:type]: [TODO:description]
    :param destination [TODO:type]: [TODO:description]
    :param md [TODO:type]: [TODO:description]
    :raises ValueError: [TODO:description]
    """
    p = utils.join_directory(directory, "icons")
    requested = md.get_all_icons()
    if p.exists():
        # get the list of icons we need to load from the metadata file
        icons = list(p.glob("**/*.svg"))
        icon_names = [os.path.basename(icon) for icon in icons]

        # if all requested icons exist in the directory
        if all([r in icon_names for r in requested]):
            for icon in icons:
                if icon.is_file():
                    shutil.copy2(icon, destination)
        else:
            missing = [r for r in requested if r not in icon_names]
            raise ValueError(f"Requested icons {missing} do not exist.")
    else:
        if len(requested) > 0:
            raise ValueError(
                f"Icon directory not found at {p}, but icons were requested."
            )
        else:
            print(
                f"Icons directory not found at {p}.\
                Not loading icons because none were requested."
            )
