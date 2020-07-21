from typing import List
from Card import Card, CardType

PLAYER_STRATS = ["Miserie", "Abondance", "Troel", "Solo"]


class Player:
    def __init__(self, discord_member, is_dealer: bool, name: str = ""):
        self.hand: List[Card] = []
        self.discord_member = discord_member
        self.partner: Player or None = None
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
        await self.discord_member.send("gij zijt den dealer")
        await self.discord_member.send("hoeveel keer wilde shufflen?")

    @staticmethod
    def get_strats():
        return PLAYER_STRATS
