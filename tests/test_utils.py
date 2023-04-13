import os
from pathlib import Path

import pytest

from extract import utils


@pytest.fixture
def sample_path():
    return Path(os.path.abspath("tests/sample_data"))


@pytest.fixture
def invalid_dir_not_exist():
    return Path(os.path.abspath("tests/sample_datad"))


def test_check_directory_valid(sample_path):
    utils.check_directory(sample_path)


def test_check_directory_not_exist(invalid_dir_not_exist):
    with pytest.raises(FileNotFoundError):
        utils.check_directory(invalid_dir_not_exist)


def test_check_directory_no_metadata(tmp_path):
    with pytest.raises(FileNotFoundError):
        utils.check_directory(tmp_path)


@pytest.fixture
def valid_args():
    parser = utils.build_parser()
    return parser.parse_args(["tests/sample_data"])


@pytest.fixture
def invalid_args():
    parser = utils.build_parser()
    return parser.parse_args(["tests/sample_datad"])


def test_check_args(valid_args):
    utils.check_args(valid_args)


def test_check_args_invalid(invalid_args):
    with pytest.raises(FileNotFoundError):
        utils.check_args(invalid_args)


@pytest.fixture
def valid_directory(valid_args):
    return utils.check_args(valid_args)


def test_load_toml(valid_directory):
    d = utils.load_toml(valid_directory)
    print(d)
