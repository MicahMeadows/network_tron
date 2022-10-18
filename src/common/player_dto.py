from dataclasses import dataclass, field

from src.common.coordinate import Coordinate
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class PlayerDTO:
    is_alive: bool
    display_character: str
    positions: list[Coordinate] = field(default_factory=list)