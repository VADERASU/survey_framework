from typing import Any, Dict, List

from bson.objectid import ObjectId


def clean_mongo_result(d: Dict[Any, Any]):
    clean = {}
    for k, val in d.items():
        if isinstance(val, ObjectId):
            clean[k] = str(val)
        else:
            clean[k] = val
    return clean


def list_to_dict(data: List[Any], key: str):
    d = {}
    for element in data:
        d[element[key]] = element
    return d
