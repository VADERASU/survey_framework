import os
from pathlib import Path

import pytest

from extract import utils


@pytest.fixture
def valid_directory():
    return Path(os.path.abspath("tests/sample_data"))


@pytest.fixture
def invalid_dir_not_exist():
    return Path(os.path.abspath("tests/sample_datad"))


@pytest.fixture
def valid_file():
    return Path(os.path.abspath("tests/sample_data/metadata.toml"))


def test_check_directory_valid(valid_directory):
    utils.check_directory(valid_directory)


def test_check_directory_not_exist(invalid_dir_not_exist):
    with pytest.raises(FileNotFoundError):
        utils.check_directory(invalid_dir_not_exist)


def test_check_directory_with_file(valid_file):
    with pytest.raises(ValueError):
        utils.check_directory(valid_file)


def test_build_directory():
    utils.build_directory("tests/sample_data")


def test_build_directory_empty():
    with pytest.raises(ValueError):
        utils.build_directory("")


def test_join_file(valid_directory):
    utils.join_file(valid_directory, "metadata.toml")


def test_join_file_not_exist(valid_directory):
    with pytest.raises(FileNotFoundError):
        utils.join_file(valid_directory, "asdfas")


def test_join_file_not_file(valid_directory):
    with pytest.raises(ValueError):
        utils.join_file(valid_directory, "images")


def test_extract_paper_from_image():
    f1 = "paper_1"
    f2 = "p_aper_2"
    assert utils.extract_paper_from_image(f1) == "paper"
    assert utils.extract_paper_from_image(f2) == "p_aper"
