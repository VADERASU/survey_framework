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
