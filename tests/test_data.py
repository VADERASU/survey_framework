import pytest

from extract import data, utils


@pytest.fixture
def sample_section():
    return {
        "images": [],
        "B": {
            "C": {"images": ["5", "6", "7", "8"]},
            "D": {"images": ["1", "2", "3", "4", "9"]},
        },
        "E": {"images": ["1", "2", "3", "4"]},
    }


@pytest.fixture
def processed_section(sample_section):
    return data.process_section("A", sample_section)


def test_process_section(sample_section):
    section = "A"

    s = data.process_section(section, sample_section)

    # check hierarchy
    """
    assert s["A"]["parent"] is None
    assert s["B"]["parent"] == "A"
    assert s["C"]["parent"] == "B"
    assert s["D"]["parent"] == "B"
    assert s["E"]["parent"] == "A"
    """

    assert s["A"]["children"] == ["B", "E"]
    assert s["B"]["children"] == ["C", "D"]
    assert s["C"]["children"] == []
    assert s["D"]["children"] == []
    assert s["E"]["children"] == []

    # check images
    assert (
        s["A"]["images"]
        == sample_section["B"]["C"]["images"]
        + sample_section["B"]["D"]["images"]
        + sample_section["E"]["images"]
    )
    assert (
        s["B"]["images"]
        == sample_section["B"]["C"]["images"]
        + sample_section["B"]["D"]["images"]
    )
    assert s["C"]["images"] == sample_section["B"]["C"]["images"]
    assert s["D"]["images"] == sample_section["B"]["D"]["images"]
    assert s["E"]["images"] == sample_section["E"]["images"]


def test_check_metadata(processed_section):
    data.check_metadata(processed_section, {})


def test_check_metadata_has_duplicate(processed_section):
    md = {}
    md.update(processed_section)
    with pytest.raises(ValueError):
        data.check_metadata(processed_section, md)


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
