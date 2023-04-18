import pytest
from pymongo import MongoClient

from database.mongo import MongoWrapper


@pytest.fixture
def mw():
    client = MongoClient(serverSelectionTimeoutMS=2000)
    return MongoWrapper(client.surveys)


# TODO: make more robust
def test_get_metadata(mw):
    r = mw.get_metadata("survey")
    print(r)


def test_get_metadata_not_exist(mw):
    with pytest.raises(ValueError):
        mw.get_metadata("asdfasdfhio")


def test_get_papers(mw):
    r = mw.get_papers("survey")
    for paper in r:
        print(paper)


def test_get_papers_not_exist(mw):
    with pytest.raises(ValueError):
        mw.get_papers("survey2357891")


def test_get_images(mw):
    r = mw.get_images("survey")
    for paper in r:
        print(paper)


def test_get_images_not_exist(mw):
    with pytest.raises(ValueError):
        mw.get_images("survey2357891")
