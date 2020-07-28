from Card import Card
from Player import Player
class Slag():
    def __init__(self,troef:int):
        self.troef=troef
        self.card_player_tuple=list()

    def lay_card(self,player:Player,card:Card):
        self.card_player_tuple.append((player,card))

    def check_winner(self):
        highest=None
        for played in self.card_player_tuple:
            if(highest==None):
                highest=played
                continue
            if(played[1].type==self.troef):
                if(highest[1].type==self.troef):
                    highest=played if played[1].value>played[1].value else highest
                else:
                    highest=played
            else:
                if(highest[1].type==self.troef):
                    continue
                else:
                    highest = played if played[1].value > played[1].value else highest
        return highest

