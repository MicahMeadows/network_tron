from abc import ABC, abstractmethod

class TronGame(ABC):

    @abstractmethod
    def set_waiting_for_players(self, is_waiting):
        pass

    @abstractmethod
    def set_on_get_players(self, on_get_players):
        pass

    @abstractmethod
    def set_on_player_move(self, on_player_move):
        pass

    @abstractmethod
    def run(self):
        pass