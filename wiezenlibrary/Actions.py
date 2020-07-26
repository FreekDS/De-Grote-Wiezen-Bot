class Action:
    def __init__(self):
        self.kwargs = []


class DealerAction(Action):
    pass


class ShuffleCards(DealerAction):
    def __init__(self):
        super().__init__()
        self.kwargs = ["times"]


class DealCards(DealerAction):
    pass


if __name__ == '__main__':
    action = DealerAction()
    print(action.action_type())