import copy

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


START_OPTIONS = ["Vraag", "Pas", "Troel", "Solo slim", "Miserie"]


class Game:
    def __init__(self):
        self.card_deck = Deck()
        self.players: List[Player] = []
        self.table: List[Card] = []
        self.state=None
        self.turn=None
        self.answered=None

    def add_player(self, player:Player):
        dealer = player.is_dealer and not self.dealer # make sure to only have one dealer
        self.players.append(player)

    async def perform_action(self, player, action):
        if(self.state==GameState.DEALING):
            if(player.is_dealer):
                self.card_deck.shuffle(int(action))
                await player.send_message("ge hebt %s keer geshoumeld"%action)
                self.deal_cards()
                await self.show_cards()
                await self.start_questions()
            else:
                await player.discord_member.send("mateke wacht eens op den dealer")
        elif(self.state==GameState.START):
            await self.handle_question(player,action)

    async def handle_question(self,player,action):
        if(self.answered!=None):
            # FIXME: zet dit terug aan voor int echt, als dat nu aan gaat kan ik niet meer met mezelf spelen
            # if(list.index(self.players,player)<=self.turn+len(self.answered())):
            #     await player.send_message("elaba gij moogt niet meer antwoorden")
            #     return
            if(action=="nee" ):
                self.answered.append(player)
                if(len(self.answered)==3-self.turn):
                    self.turn+=1
                    # FIXME hier moet iets om naar volgende beurt te gaan
                else:
                    await self.players[self.turn + len(self.answered) + 1].send_message(
                        "den %s vraagt, wilt ge mee? ja/nee" %
                        self.players[self.turn].name)

            elif(action=="ja"):

                leftover=copy.copy(self.players)
                temp=list.index(self.players,player)
                leftover.pop(temp)
                leftover.pop(self.turn)
                await self.send_to(self.players,"%s heeft een coalitie gemaakt met %s, dus nu moeten %s en %s maar samen"%
                                   (self.players[self.turn].name,player.name,leftover[0].name,leftover[1].name))
                #FIXME hier met iets staan om mensen te koppelen en verder te gaan
        else:
            if(action=="Vraag"):
                self.answered=list()
                await self.players[self.turn+len(self.answered)+1].send_message("den %s vraagt, wilt ge mee? ja/nee"%
                                                      self.players[self.turn].name)



    async def start_game(self):
        self.state = GameState.DEALING
        await self.dealer.ask_shuffles()

    async def start_questions(self):
        self.state = GameState.START
        for idx,player in enumerate(self.players):
            if(player.must_start):
                self.turn=0
                newlist=self.players[idx:]
                newlist+=self.players[:idx]
                self.players=newlist
                break
        await self.players[self.turn].send_message("wat wilde doen met uw kaarten: %s"%START_OPTIONS)


    @property
    def dealer(self):
        for player in self.players:
            if player.is_dealer:
                return player
        return None

    def get_wiezen_speler(self,identifier:str):
        for player in self.players:
            if(player.identifier==identifier):
                return player
        return None

    def deal_cards(self):
        while(len(self.card_deck.cards)!=0):
            for player in self.players:
                player.give_card(self.card_deck.get_card())

    async def show_cards(self):
        for player in self.players:
            await player.send_message(player.show_cards())

    async def send_to(self,players,message):
        for player in players:
            await player.send_message(message)


