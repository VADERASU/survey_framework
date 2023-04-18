import pytest

from extract import data, utils


@pytest.fixture
def valid_args():
    parser = utils.build_parser()
    args = parser.parse_args(["tests/sample_data"])

    return utils.check_args(args)


# TODO: finish test
def test_load_images(valid_args):
    dir, dest = valid_args
    images = data.load_images(dir, dest)
    # check that files have been copied to dest


# TODO: implement
def test_load_images_no_images():
    pass


def test_map_image_keywords():
    pass
