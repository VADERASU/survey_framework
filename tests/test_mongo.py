import pytest
from pymongo import MongoClient

from database.mongo import MongoWrapper


@pytest.fixture
def mw():
    client = MongoClient(serverSelectionTimeoutMS=2000)
    return MongoWrapper(client.surveys)


# TODO: make more robust
def test_get_metadata_hierarchy(mw):
    r = mw.get_metadata_hierarchy()
    print(r)
