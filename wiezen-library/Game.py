from Deck import Deck
from typing import List
from Player import Player
from Card import Card
import enum


class GameState(enum.Enum):
    DEALING = 0
    START = 1
    PLAYING = 2
    END = 3


START_OPTIONS = ["Vraag", "Pas", "Solo slim", "Miserie"]


class Game:
    def __init__(self):
        self.card_deck = Deck()
        self.players: List[Player] = []
        self.table: List[Card] = []

    def add_player(self, discord_member, dealer=False):
        dealer = dealer and not self.dealer # make sure to only have one dealer
        new_player = Player(discord_member, dealer)
        self.players.append(new_player)

    def perform_action(self, player, action):
        pass

    @property
    def dealer(self):
        for player in self.players:
            if player.is_dealer:
                return player
        return None
