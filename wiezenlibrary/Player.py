import enum
from abc import ABC, abstractmethod
from typing import List
from wiezenlibrary.Card import Card, CardType


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
        self.is_dealer: bool = is_dealer
        self.name: str = name

        self.last_played: Card or None = None

    def give_card(self, card: Card):
        self.hand.append(card)

    def play_card(self, card: Card):
        self.hand.remove(card)

    def show_cards(self):
        return self.hand

    @property
    def must_start(self):
        return self.has_card(Card(CardType.SCHOPPEN, 2))

    async def ask_shuffles(self):
        await self.send_message("gij zijt den dealer")
        await self.send_message("hoeveel keer wilde shufflen?")

    async def send_message(self, message, is_file=False):
        raise NotImplemented()

    def get_card(self, index):
        card = self.hand[index]
        return card

    def remove_card(self, index):
        card = self.hand[index]
        self.hand.remove(card)

    def count_aces(self):
        count = 0
        for card in self.hand:
            if card.value == 1:
                count += 1
        return count

    def get_aces(self):
        aces = list()
        for card in self.hand:
            if card.value == 1:
                aces.append(card)
        return aces

    def has_card(self, card):
        return card in self.hand

    def has_type(self, type):
        has_type = False
        for card in self.hand:
            if (card.type == type):
                has_type = True
        return has_type
