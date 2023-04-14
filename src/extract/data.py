import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, TypedDict

import bibtexparser
import toml
from typeguard import typechecked

from extract import utils


class Metadata(TypedDict):
    parent: Optional[str]
    images: List[str]


MetadataDict = Dict[str, Metadata]


@typechecked
def check_metadata(
    section: MetadataDict,
    metadata: MetadataDict,
):
    """
    Checks a newly created metadata dictionary for duplicates
    in the existing one.

    :param section: The newly created metadata dictionary.
    :param metadata: The existing metadata dictionary we plan to add to.
    :raises ValueError: Raised if duplicate section names exist.
    """
    new_sections = list(section.keys())
    sections = list(metadata.keys())

    for new_section in new_sections:
        if new_section in sections:
            raise ValueError(f"Duplicate metadata tag found: {new_section}.")


@typechecked
def process_metadata(metadata: Dict[str, Any]) -> MetadataDict:
    """
    Builds a hierarchy based on the metadata passed from the TOML file.

    :param metadata: TOML metadata.
    :return: A dictionary of metadata keys to their values
    which contain parents and images.
    """
    md = {}
    for section in metadata.keys():
        s = process_section(section, metadata[section])
        check_metadata(s, md)
        md.update(s)
    return md


@typechecked
def process_section(
    section: str, value: Dict[str, Any], parent: Optional[str] = None
) -> MetadataDict:
    """
    Given a metadata section, traverse through the nested dictionary to
    build its hierarchy.

    :param section: Name of the header section.
    :param value: The dictionary associated with the section.
    :param parent: Optional, passed to children to identify parent metadata
    section.
    :return: A dictionary of strings to Metadata objects.
    """
    images = []
    sections = {}
    for key in value.keys():
        if key == "images":
            images = value[key]
        else:
            s_sections = process_section(key, value[key], section)
            sections.update(**s_sections)

    sections[section] = {"parent": parent, "images": images}
    return sections


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
