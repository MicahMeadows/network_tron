from dataclasses import dataclass
from mimetypes import init
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Coordinate:
    x: int
    y: int