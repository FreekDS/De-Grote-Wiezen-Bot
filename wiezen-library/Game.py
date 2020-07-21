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
        self.state=None

    def add_player(self, discord_member, dealer=False):
        dealer = dealer and not self.dealer # make sure to only have one dealer
        new_player = Player(discord_member, dealer)
        self.players.append(new_player)

    async def perform_action(self, player, action):
        if(self.state==GameState.DEALING):
            if(player.is_dealer):
                self.card_deck.shuffle(int(action))
                await player.discord_member.send("ge hebt %s keer geshoumeld"%action)
            else:
                await player.discord_member.send("mateke wacht eens op den dealer")

    async def start_game(self):
        self.state = GameState.DEALING
        await self.dealer.ask_shuffles()

    @property
    def dealer(self):
        for player in self.players:
            if player.is_dealer:
                return player
        return None

    def get_wiezen_speler(self,discord):
        for player in self.players:
            if(player.discord_member==discord):
                return player
        return None

