import argparse
import os
import re
import shutil
from pathlib import Path
from typing import Union

import bibtexparser
import toml
from typeguard import typechecked


def get_api_directory():
    source = Path(__file__).resolve()
    return source.parent.parent.joinpath("api").joinpath("images")


def build_parser():
    parser = argparse.ArgumentParser(prog="SurveyPaperExtractor")
    parser.add_argument("directory")
    parser.add_argument("-i", "--image-directory", default=get_api_directory())
    return parser


# why not return directory here?
@typechecked
def check_directory(directory: Path):
    if not directory.exists():
        raise FileNotFoundError(f"{directory} does not exist.")

    if not directory.is_dir():
        raise ValueError(f"{directory} is not a directory.")


@typechecked
def not_found(directory: Path, description: str):
    raise FileNotFoundError(f"{directory} does not contain {description}")


@typechecked
def load_toml(directory: Path):
    p = directory.joinpath("metadata.toml")
    if not p.exists():
        not_found(directory, "metadata.toml")
    return toml.load(p)


@typechecked
def load_bibtex(directory: Path):
    p = directory.joinpath("papers.bib")
    if not p.exists():
        not_found(directory, "papers.bib")
    data = None
    with open(p) as bib_tex:
        data = bibtexparser.load(bib_tex)
    return data


# TODO: test, move to metadata?
@typechecked
def load_images(directory: Path, image_directory: Path):
    p = directory.joinpath("images")
    check_directory(p)
    img_types = ("jpg", "jpeg", "png", "gif")
    extracted = {}
    for img_type in img_types:
        images = list(p.glob(f"**/*.{img_type}"))
        for image in images:
            if image.is_file():
                shutil.copy2(image, image_directory)
                f_name = os.path.basename(image)
                paper = extract_paper_from_image(f_name)
                extracted[f_name] = {
                    "keywords": [],
                    "paper": paper,
                }

    if len(extracted) == 0:
        raise ValueError(f"{p} was empty.")

    return extracted


def check_args(args):
    directory = Path(os.path.abspath(args.directory))
    image_directory = Path(os.path.abspath(args.image_directory))
    check_directory(directory)
    check_directory(image_directory)
    return directory, image_directory


def extract_paper_from_image(f_name: Union[Path, str]):
    """
    images should be named
    {citation_key}{_ID}
    _ID is optional and is only used to
    prevent naming conflicts in the filesystem
    """

    name, _ = os.path.splitext(f_name)
    return re.sub("_([^_]*)$", "", name)
