from wiezenlibrary.Player import Player
from wiezenlibrary.Deck import Deck
from wiezenlibrary.Card import Card
from wiezenlibrary.Game import GameState
from typing import List
import enum


class WiezenException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)


class Command(object):
    def __init__(self, obj):
        self._obj = obj

    def execute(self):
        raise NotImplementedError()


class ShuffleCardsCommand(Command):
    def __init__(self, obj: Deck, times):
        super().__init__(obj)
        self.times = times

    def execute(self):
        self._obj.shuffle(self.times)


class Actions(enum.Enum):
    AskShuffleCount = "askShuffleCount"


class AsyncShuffleCardsCommand(ShuffleCardsCommand):
    def __init__(self, obj: Deck, times):
        super().__init__(obj, times)

    async def execute(self):
        super().execute()


class PlayCard(Command):
    def __init__(self, obj, card: Card):
        super().__init__(obj)
        self.card = card

    def execute(self):
        pass


class BaseGame:
    def __init__(self):
        self.state: GameState = GameState.DEALING
        self.players: List[Player] = []

        self.deck: Deck = Deck()
        self.table = None

        self.required_action = None

        self.game_active = True
        self.command_queue: List[Command] = list()

    @property
    def dealer(self):
        for player in self.players:
            if player.is_dealer:
                return player
        else:
            return None

    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)

    def _can_start(self):
        player_count_ok = len(self.players) == 4
        has_dealer = self.dealer is not None
        return player_count_ok and has_dealer

    def progress_step(self) -> Actions:
        if not self._can_start():
            raise WiezenException("Make sure to have enough players")
        if self.state == GameState.DEALING:
            return self._deal_state()
        elif self.state == GameState.START:
            pass
        elif self.state == GameState.PLAYING:
            pass
        elif self.state == GameState.END:
            pass
        else:
            raise WiezenException("Unknown GameState")

    def _deal_state(self) -> Actions:
        self.required_action = Actions.AskShuffleCount
        return Actions.AskShuffleCount

    def _start_state(self):
        raise NotImplementedError()

    def _playing_state(self):
        raise NotImplementedError()

    def _end_state(self):
        raise NotImplementedError()

    def end_dealing(self):
        self.state = GameState.START

    def end_start(self):
        self.state = GameState.PLAYING

    def end_playing(self):
        self.state = GameState.END

    def process_commands(self):
        while not self.game_active:
            command = self.command_queue.pop(0)
            command.execute()
