from AbstractStrategy import AbstractStrategy

class DansenAloneStrategy(AbstractStrategy):

    def __init__(self):
        return

    def get_oposite(self):
        from DansenTogetherStrategy import DansenTogetherStrategy
        return DansenTogetherStrategy()

    def get_scores(self, slag_amount):
        return 15

    def check_win(self, teams_wins: int, enemy_wins: int):
        return teams_wins >= 9
