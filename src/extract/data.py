import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, TypedDict

import bibtexparser
import toml
from typeguard import typechecked

from extract import utils
from extract.tree import MetadataTree


class Metadata(TypedDict):
    children: List[str]
    images: List[str]


MetadataDict = Dict[str, Metadata]


# TODO: should test initial metadata dictionary only
@typechecked
def check_metadata(
    metadata: MetadataDict,
):
    """
    Checks a newly created metadata dictionary for duplicates
    in the existing one.

    :param section: The newly created metadata dictionary.
    :param metadata: The existing metadata dictionary we plan to add to.
    :raises ValueError: Raised if duplicate section names exist.
    """
    pass


def build_hierarchy(metadata: Dict[str, Any]):
    """
    Builds metadata tree for the given dictionary.

    :param metadata: The metadata dictionary to process.
    """
    return MetadataTree(metadata)


@typechecked
def load_toml(directory: Path):
    p = utils.join_file(directory, "metadata.toml")
    return toml.load(p)


@typechecked
def load_bibtex(directory: Path):
    p = utils.join_file(directory, "papers.bib")
    data = None
    with open(p) as bib_tex:
        data = bibtexparser.load(bib_tex)
    return data


class Image(TypedDict):
    keywords: List[str]
    paper: str


@typechecked
def load_images(directory: Path, destination: Path) -> Dict[str, Image]:
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
                extracted[f_name] = {
                    "keywords": [],
                    "paper": paper,
                }

    if len(extracted) == 0:
        raise ValueError(
            f"{p} does not contain any of the supported\
            image types {img_types}."
        )

    return extracted


def map_image_keywords(images: Dict[str, Image], md: MetadataTree):
    """
    Maps images to their keywords using a Metadata tree.

    :param images: Dictionary of image file names to data.
    :param md: MetadataTree; see tree.py
    """
    for image, image_md in images.items():
        for keyword in md.all_nodes():
            if keyword.tag != "root":
                kw_images = md.get_keyword_images(keyword.tag)
                if image in kw_images:
                    image_md["keywords"].append(keyword.tag)
