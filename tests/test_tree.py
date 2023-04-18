import pytest

from extract.tree import MetadataTree
from extract.utils import section_names


@pytest.fixture
def sample_md():
    return {
        "A": {
            "images": [],
            "B": {
                "C": {"images": ["5", "6", "7", "8"]},
                "D": {"images": ["1", "2", "3", "4", "9"]},
            },
            "E": {"images": ["1", "2", "3", "4"]},
        },
        "F": {
            "G": {"images": ["10", "11", "12"]},
            "H": {"images": ["13", "14", "15"]},
        },
    }


@pytest.fixture
def t(sample_md):
    return MetadataTree(sample_md)


def tags(arr):
    return list(map(lambda e: e.tag, arr))


def children(t, tag):
    c = tags(t.children(tag))
    c.sort()
    return c


def test_build_tree(sample_md, t):
    leaves = tags(t.leaves())
    leaves.sort()
    assert leaves == ["C", "D", "E", "G", "H"]

    assert children(t, "A") == section_names(sample_md["A"])
    assert children(t, "B") == section_names(sample_md["A"]["B"])
    assert children(t, "C") == []
    assert children(t, "D") == []
    assert children(t, "E") == section_names(sample_md["A"]["E"])
    assert children(t, "F") == section_names(sample_md["F"])

    assert tags(t.siblings("A")) == ["F"]
    assert tags(t.siblings("C")) == ["D"]
    assert tags(t.siblings("B")) == ["E"]


def test_get_keyword_images(t):
    im = t.get_keyword_images("A")
    im.sort()
    assert im == ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

# TODO: make more robust
def test_to_dict(t):
    d = t.to_dict()
    assert d == {
        "name": "root",
        "children": [
            {
                "name": "A",
                "children": [
                    {
                        "name": "B",
                        "children": [
                            {"name": "C", "children": []},
                            {"name": "D", "children": []},
                        ],
                    },
                    {"name": "E", "children": []},
                ],
            },
            {
                "name": "F",
                "children": [
                    {"name": "G", "children": []},
                    {"name": "H", "children": []},
                ],
            },
        ],
    }
