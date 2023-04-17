import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, TypedDict

import bibtexparser
import toml
from typeguard import typechecked

from extract import utils


class Metadata(TypedDict):
    children: List[str]
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


def get_header_sections(metadata: MetadataDict):
    """
    Gets the top level sections from the metadata dictionary.

    :param metadata: The metadata dictionary.
    """
    names = list(metadata.keys())
    children = []
    for data in metadata.values():
        for name in names:
            if name in data["children"]:
                children.append(name)
    return list(filter(lambda e: e not in children, names))


def nest(metadata: MetadataDict, header: str):
    """
    Returns a header as an object containing its children nested and its name.

    :param metadata: Metadata dictionary.
    :param header: The name of the section.
    """
    children = metadata[header]["children"]
    data = []
    for child in children:
        if len(metadata[child]["children"]) > 0:
            data.append({"name": child, "children": nest(metadata, child)})
        else:
            data.append({"name": child, "children": []})
    return data


def build_hierarchy(metadata: MetadataDict):
    """
    Builds a hierarchy from the metadata dictionary.

    :param metadata: A metadata dictionary.
    """
    headers = get_header_sections(metadata)
    document = []
    for header in headers:
        document.append({"name": header, "children": nest(metadata, header)})
    return document


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
    section: str,
    value: Dict[str, Any],
) -> MetadataDict:
    """
    Given a metadata section, traverse through the nested dictionary to
    build its hierarchy.

    :param section: Name of the header section.
    :param value: The dictionary associated with the section.
    :return: A dictionary of strings to Metadata objects.
    """
    images = []
    sections = {}
    children = []
    for key in value.keys():
        if key == "images":
            images.extend(value[key])
        else:
            s_sections = process_section(key, value[key])
            sections.update(**s_sections)
            children.append(key)
            images.extend(s_sections[key]["images"])

    sections[section] = {"children": children, "images": images}
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
