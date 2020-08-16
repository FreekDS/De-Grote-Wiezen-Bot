from AbstractStrategy import AbstractStrategy

class SoloAloneStrategy(AbstractStrategy):

    def __init__(self):
        return

    def get_oposite(self):
        from SoloTeamStrategy import SoloTeamStrategy
        return SoloTeamStrategy()

    def get_scores(self, slag_amount):
        return 75

    def check_win(self, teams_wins: int, enemy_wins: int):
        return teams_wins >= 13
