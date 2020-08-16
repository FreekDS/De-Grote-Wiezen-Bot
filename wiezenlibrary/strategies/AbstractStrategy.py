import abc


class AbstractStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_oposite(self):
        pass

    @abc.abstractmethod
    def get_scores(self, slag_amount):
        pass

    @abc.abstractmethod
    def check_win(self, teams_wins: int, enemy_wins: int):
        pass
