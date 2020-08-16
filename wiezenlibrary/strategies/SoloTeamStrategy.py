from AbstractStrategy import AbstractStrategy

class SoloTeamStrategy(AbstractStrategy):

    def __init__(self):
        return

    def get_oposite(self):
        from SoloAloneStrategy import SoloAloneStrategy
        return SoloAloneStrategy()

    def get_scores(self, slag_amount):
        return 5

    def check_win(self, teams_wins: int, enemy_wins: int):
        return teams_wins >= 1
