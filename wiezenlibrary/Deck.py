import random

from wiezenlibrary.Card import Card


class Deck:
    def __init__(self):
        self.cards = []
        self.reset()

    def shuffle(self, times=1):
        for i in range(0, times):
            random.shuffle(self.cards)

    def get_card(self):
        return self.cards.pop()

    def reset(self):
        self.cards = [Card(t, v) for t in range(0, 4) for v in range(1, 14)]

    def __repr__(self):
        return str(self.cards)


if __name__ == '__main__':
    d = Deck()
    print(d)
