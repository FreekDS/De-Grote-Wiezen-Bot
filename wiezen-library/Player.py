from typing import List
from Card import Card

PLAYER_STRATS = ["Miserie", "Abondance", "Troel", "Solo"]


class Player:
    def __init__(self):
        self.hand: List[Card] = []
        self.partner: Player or None = None
        self.round_wins: int = 0
        self.strategy: str or None = None

    def give_card(self, card: Card):
        self.hand.append(card)

    def play_card(self, card: Card):
        self.hand.remove(card)

    def show_cards(self):
        pass

    @staticmethod
    def get_strats():
        return PLAYER_STRATS
