from . import player
from gojos import model

class Tournament:
    def __init__(self, name, subject_name: str, perma_id: str):
        self.name = name
        self.perma_id = perma_id
        self.subject_name = subject_name


class GrandSlam(Tournament):
    pass


class Course:
    def __init__(self, name, par, country_symbol):
        self.name = name
        self.par = par
        self.country_symbol = country_symbol



class Cut:

    def below_cut_line(self, player_score: player.PlayerScore):
        return self.player_below_cut(player_score)

    def relative_to_cut(self, position):
        return self._position_from_cut(position)

class CutTop60AndTies(Cut):
    cut_position = 60

    def _position_from_cut(self, position):
        if isinstance(position, model.PlayerState):
            return -1
        if position == self.cut_position:
            return 0
        return self.cut_position - position


