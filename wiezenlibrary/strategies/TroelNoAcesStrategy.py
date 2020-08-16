from AbstractStrategy import AbstractStrategy

class TroelNoAcesStrategy(AbstractStrategy):

    def __init__(self):
        return

    def get_oposite(self):
        from TroelAcesStrategy import TroelAcesStrategy
        return TroelAcesStrategy()

    def get_scores(self, slag_amount):
        return 10

    def check_win(self, teams_wins: int, enemy_wins: int):
        return teams_wins >= 5
