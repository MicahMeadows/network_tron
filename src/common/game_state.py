from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from src.common.player_dto import PlayerDTO

@dataclass_json
@dataclass
class GameState:
    players: list[PlayerDTO] = field(default_factory=list)