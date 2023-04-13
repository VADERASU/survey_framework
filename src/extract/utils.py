import argparse
import os
from pathlib import Path

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

    # check that it contains metadata and images folder
    contents = os.listdir(directory)

    if "metadata.toml" not in contents:
        raise FileNotFoundError(
            f"{directory} does not contain an images directory."
        )


@typechecked
def load_toml(directory: Path):
    p = directory.joinpath("metadata.toml")
    if not p.exists():
        raise FileNotFoundError(f"{directory} does not contain metadata.toml.")
    return toml.load(p)


def check_args(args):
    directory = Path(os.path.abspath(args.directory))
    check_directory(directory)
    return directory
