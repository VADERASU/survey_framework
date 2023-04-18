import argparse
import os
import re
from pathlib import Path
from typing import Union

from typeguard import typechecked


def section_names(d):
    return list(filter(lambda e: e != "images", d.keys()))


def get_api_image_dir():
    """
    Assumes that the image directory for the back-end will be in
    ../../api/images
    """
    source = Path(__file__).resolve()
    return source.parent.parent.joinpath("api").joinpath("images")


def build_parser():
    parser = argparse.ArgumentParser(prog="SurveyPaperExtractor")
    parser.add_argument("directory")
    parser.add_argument("-i", "--image-directory", default=get_api_image_dir())
    return parser


@typechecked
def check_directory(directory: Path):
    """
    Check if directory exists and is a directory.

    :param directory: Path to directory to check.
    :raises FileNotFoundError: Raised if directory does not exist.
    :raises ValueError: Raised if directory is not a directory.
    """
    if not directory.exists():
        raise FileNotFoundError(f"{directory} does not exist.")

    if not directory.is_dir():
        raise ValueError(f"{directory} is not a directory.")


@typechecked
def join_directory(directory: Path, dir_name: str) -> Path:
    """
    Given a directory and string, returns a Path to the directory associated
    with the string.

    :param directory: The directory to join to.
    :param dir_name: Name of the directory.
    :return: Path to dir_name.
    """
    p = directory.joinpath(dir_name)
    check_directory(p)
    return p


@typechecked
def build_directory(path: Union[Path, str]):
    """
    Builds an absolute path from a string.

    :param path: The name of the path.
    :raises ValueError: If the path was empty.
    """
    if path == "":
        raise ValueError("Specified path was empty.")
    directory = Path(os.path.abspath(path))
    check_directory(directory)
    return directory


@typechecked
def join_file(directory: Path, f_name: str) -> Path:
    """
    Given a directory and string, returns a Path to the file associated with
    the string.

    :param directory: The directory to join to.
    :param f_name: Name of the file.
    :return: Path to f_name.
    :raises FileNotFoundError: Raised if file does not exist.
    :raises ValueError: Raised if path does not point to file.
    """
    p = directory.joinpath(f_name)
    if not p.exists():
        raise FileNotFoundError(f"{directory} does not contain {f_name}")

    if not p.is_file():
        raise ValueError(f"{f_name} is not a file.")

    return p


def check_args(args):
    """
    Checks args from arg_parse.
    """
    directory = build_directory(args.directory)
    image_directory = build_directory(args.image_directory)
    return directory, image_directory


@typechecked
def extract_paper_from_image(f_name: Union[Path, str]) -> str:
    """
    Determines an image's associated paper from its filename.
    Images should be named {citation_key}{_ID} _ID is optional
    and is only used to prevent naming conflicts in the filesystem.

    :param f_name: The filename to extract.
    :returns: Name of the paper associated with the image.
    """

    name, _ = os.path.splitext(f_name)
    return re.sub("_([^_]*)$", "", name)
