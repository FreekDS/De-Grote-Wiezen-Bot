from AbstractStrategy import AbstractStrategy

class TroelAcesStrategy(AbstractStrategy):

    def __init__(self):
        return

    def get_oposite(self):
        from TroelNoAcesStrategy import TroelNoAcesStrategy
        return TroelNoAcesStrategy()

    def get_scores(self, slag_amount):
        return 5

    def check_win(self, teams_wins: int, enemy_wins: int):
        return teams_wins >= 7
