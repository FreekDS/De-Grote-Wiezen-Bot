import copy

from wiezenlibrary.Deck import Deck
from typing import List
from wiezenlibrary.Player import Player
from wiezenlibrary.Card import Card
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

    def add_player(self, discord_member, dealer=False):
        dealer = dealer and not self.dealer # make sure to only have one dealer
        new_player = Player(discord_member, dealer)
        self.players.append(new_player)

    async def perform_action(self, player, action):
        if(self.state==GameState.DEALING):
            if(player.is_dealer):
                self.card_deck.shuffle(int(action))
                await player.discord_member.send("ge hebt %s keer geshoumeld"%action)
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
            #     await player.discord_member.send("elaba gij moogt niet meer antwoorden")
            #     return
            if(action=="nee" ):
                self.answered.append(player)
                if(len(self.answered)==3-self.turn):
                    self.turn+=1
                    # FIXME hier moet iets om naar volgende beurt te gaan
                else:
                    await self.players[self.turn + len(self.answered) + 1].discord_member.send(
                        "den %s vraagt, wilt ge mee? ja/nee" %
                        self.players[self.turn].discord_member.name)

            elif(action=="ja"):

                leftover=copy.copy(self.players)
                temp=list.index(self.players,player)
                leftover.pop(temp)
                leftover.pop(self.turn)
                await self.send_to(self.players,"%s heeft een coalitie gemaakt met %s, dus nu moeten %s en %s maar samen"%
                                   (self.players[self.turn].discord_member.name,player.discord_member.name,leftover[0].discord_member.name,leftover[1].discord_member.name))
                #FIXME hier met iets staan om mensen te koppelen en verder te gaan
        else:
            if(action=="Vraag"):
                self.answered=list()
                await self.players[self.turn+len(self.answered)+1].discord_member.send("den %s vraagt, wilt ge mee? ja/nee"%
                                                      self.players[self.turn].discord_member.name)



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
        await self.players[self.turn].discord_member.send("wat wilde doen met uw kaarten: %s"%START_OPTIONS)


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

    def deal_cards(self):
        while(len(self.card_deck.cards)!=0):
            for player in self.players:
                player.give_card(self.card_deck.get_card())

    async def show_cards(self):
        for player in self.players:
            await player.discord_member.send(player.show_cards())

    async def send_to(self,players,message):
        for player in players:
            await player.discord_member.send(message)


