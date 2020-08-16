from AbstractStrategy import AbstractStrategy

class MiserieAloneStrategy(AbstractStrategy):

    def __init__(self):
        return

    def get_oposite(self):
        from MiserieTogetherStrategy import MiserieTogetherStrategy
        return MiserieTogetherStrategy()

    def get_scores(self, slag_amount):
        return 21

    def check_win(self, teams_wins: int, enemy_wins: int):
        return enemy_wins >= 13
