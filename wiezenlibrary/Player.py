from abc import ABC, abstractmethod
from typing import List
from wiezenlibrary.Card import Card, CardType

PLAYER_STRATS = ["Miserie", "Abondance", "Troel", "Solo"]


class Player(ABC):
    def __init__(self, name: str, identifier: str, is_dealer: bool):
        """
        init of ths abstract class
        :param name: the name for this user
        :param identifier: the unique identifier for this user
        :param is_dealer: a bool denoting whether the player is a dealer
        """
        self.hand: List[Card] = []
        self.identifier = identifier
        self.round_wins: int = 0
        self.strategy: str or None = None
        self.is_dealer: bool = is_dealer
        self.name: str = name

    def give_card(self, card: Card):
        self.hand.append(card)

    def play_card(self, card: Card):
        self.hand.remove(card)

    def show_cards(self):
        return self.hand

    @property
    def must_start(self):
        return Card(CardType.SCHOPPEN, 2) in self.hand

    async def ask_shuffles(self):
        await self.send_message("gij zijt den dealer")
        await self.send_message("hoeveel keer wilde shufflen?")

    @staticmethod
    def get_strats():
        return PLAYER_STRATS

    async def send_message(self, message):
        raise NotImplemented()

    def count_aces(self):
        count=0
        for card in self.hand:
            if card.value==1:
               count+=1
        return count

    def has_card(self,card):
        return card in self.hand
