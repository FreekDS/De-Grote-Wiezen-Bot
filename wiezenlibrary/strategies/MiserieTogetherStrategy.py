from AbstractStrategy import AbstractStrategy

class MiserieTogetherStrategy(AbstractStrategy):

    def __init__(self):
        return

    def get_oposite(self):
        from MiserieAloneStrategy import MiserieAloneStrategy
        return MiserieAloneStrategy()

    def get_scores(self, slag_amount):
        return 7

    def check_win(self, teams_wins: int, enemy_wins: int):
        return teams_wins >= 1
