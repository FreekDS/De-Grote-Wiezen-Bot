from typing import List, Tuple

from wiezenlibrary.Card import Card, CardType
from wiezenlibrary.Player import Player


class Slag:
    def __init__(self, troef: CardType or int, first=False):
        self.troef: CardType = troef
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
                highest = self.check_with_troef_card(highest, played)

            elif played[1].type == self.type:
                if highest[1].type == self.troef:
                    continue
                else:
                    highest = played if played[1] > highest[1] else highest
        return highest

    def check_with_troef_card(self, highest, played):
        if highest[1].type == self.troef:
            highest = played if played[1] > highest[1] else highest
        else:
            highest = played
        return highest
