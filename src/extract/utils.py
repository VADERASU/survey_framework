import argparse
import os
from pathlib import Path

import bibtexparser
import toml
from typeguard import typechecked


def build_parser():
    parser = argparse.ArgumentParser(prog="SurveyPaperExtractor")
    parser.add_argument("directory")
    return parser


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


@typechecked
def load_images(directory: Path):
    p = directory.joinpath("images")
    check_directory(p)
    img_types = ("jpg", "jpeg", "png", "gif")
    extracted = {}
    for img_type in img_types:
        images = list(p.glob(f"**/*.{img_type}"))
        for image in images:
            if image.is_file():
                # copy over to api/images, get path
                f_name = os.path.basename(image)
                extracted[f_name] = {}
    if len(extracted) == 0:
        raise FileNotFoundError(f"{p} was empty.")

    return extracted


def check_args(args):
    directory = Path(os.path.abspath(args.directory))
    check_directory(directory)
    return directory
