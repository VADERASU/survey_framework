from typing import Dict, List, Optional, TypedDict


class Metadata(TypedDict):
    images: List[str]
    color: Optional[str]
    icon: Optional[str]


MetadataDict = Dict[str, Metadata]
