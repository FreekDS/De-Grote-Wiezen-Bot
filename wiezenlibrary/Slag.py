from wiezenlibrary.Card import Card
from wiezenlibrary.Player import Player
from typing import List, Tuple


class Slag:
    def __init__(self, troef: int, first=False):
        self.troef = troef
        # The type everyone must follow unless they cant
        self.type = None
        self.first = first
        self.card_player_tuple: List[Tuple[Player, Card]] = list()

    def lay_card(self, player: Player, card: Card):
        if self.type is None: self.type = card.type
        self.card_player_tuple.append((player, card))

    def check_winner(self):
        highest = None
        for played in self.card_player_tuple:
            if highest is None:
                highest = played
                continue
            if played[1].type == self.troef:
                if highest[1].type == self.troef:
                    highest = played if played[1] > highest[1] else highest
                else:
                    highest = played
            else:
                if highest[1].type == self.troef:
                    continue
                else:
                    highest = played if played[1] > highest[1] else highest
        return highest
