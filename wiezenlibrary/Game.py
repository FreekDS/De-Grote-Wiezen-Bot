import copy

from discord import File

from ImageGenerator import ImageGenerator
from wiezenlibrary.Deck import Deck
from typing import List
from wiezenlibrary.Player import Player
from wiezenlibrary.Card import Card
import enum

from wiezenlibrary.Card import CardType
from wiezenlibrary.Team import Team


class GameState(enum.Enum):
    DEALING = 0
    START = 1
    PLAYING = 2
    END = 3


# Other game options: TROEL <= gets triggered when someone has 3 aces
START_OPTIONS = ["Vraag", "Pas", "Solo slim", "Miserie"]


class Game:
    def __init__(self):
        self.card_deck = Deck()
        self.teams = list()
        self.players: List[Player] = []
        self.table: List[Card] = []
        self.state = None
        self.turn = None
        self.answered = None

    def add_player(self, player: Player):
        dealer = player.is_dealer and not self.dealer  # make sure to only have one dealer
        self.players.append(player)

    async def perform_action(self, player, action):
        if self.state == GameState.DEALING:
            if player.is_dealer:
                self.card_deck.shuffle(int(action))
                await player.send_message("ge hebt %s keer geshoumeld" % action)
                self.deal_cards()
                await self.show_cards()
                await self.start_questions()
            else:
                await player.discord_member.send("mateke wacht eens op den dealer")
        elif self.state == GameState.START:
            await self.handle_question(player, action)

    async def handle_question(self, player, action):

        if self.answered is not None:

            if self.players[self.turn + len(self.answered) + 1].identifier != player.identifier:
                await self.send_to([player], "Elaba stopt eens met onze bot kapot te maken")
                return
            # FIXME: zet dit terug aan voor int echt, als dat nu aan gaat kan ik niet meer met mezelf spelen
            # if(list.index(self.players,player)<=self.turn+len(self.answered())):
            #     await player.send_message("elaba gij moogt niet meer antwoorden")
            #     return
            if action == "nee":
                await self.handle_no_answer(player)
            elif action == "ja":
                await self.handle_Yes_answer(player)
        else:
            if self.players.index(player) != self.turn:
                await self.send_to([player], "Elaba stopt eens met onze bot kapot te maken")
                return
            if action == "Vraag":
                await self.handle_vraag_answer()
            elif action == "Pas":
                await self.handle_pas_answer(player)

    async def handle_pas_answer(self, player):
        await self.send_to(self.players, "den %s zegt dat hem moet passen van zijn moeder" % player.name)
        await self.advance_turn()
        await self.send_card_question()

    async def handle_vraag_answer(self):
        self.answered = list()
        await self.players[self.turn + len(self.answered) + 1].send_message(
            "den %s vraagt, wilt ge mee? ja/nee" %
            self.players[self.turn].name)

    async def handle_Yes_answer(self, player):

        await self.send_to(self.players,
                           "%s heeft een coalitie gemaakt met %s" %
                           (self.players[self.turn].name, player.name))
        self.make_team([self.players[self.turn], player])
        self.state = GameState.PLAYING

    async def handle_no_answer(self, player):
        self.answered.append(player)
        if len(self.answered) == 3 - self.turn:
            await self.send_to(self.players, "niemand wilt mee met den %s, sad" % self.players[self.turn].name)
            await self.advance_turn()
            self.answered = None
            await self.send_card_question()
        else:
            await self.players[self.turn + len(self.answered) + 1].send_message(
                "den %s vraagt, wilt ge mee? ja/nee" %
                self.players[self.turn].name)

    async def advance_turn(self):
        self.turn += 1
        if self.turn > 3:
            await self.send_to(self.players, "allé dat we niet willen spelen dan beginnen we maar opnieuw hé")
            self.state = GameState.DEALING
            self.turn = 0
            await self.dealer.ask_shuffles()

    async def start_game(self):
        self.state = GameState.DEALING
        await self.dealer.ask_shuffles()

    async def start_questions(self):
        self.state = GameState.START
        if await self.check_troel():
            self.state = GameState.PLAYING
        else:
            for idx, player in enumerate(self.players):
                if player.must_start:
                    self.turn = 0
                    newlist = self.players[idx:]
                    newlist += self.players[:idx]
                    self.players = newlist
                    break
            await self.send_card_question()

    async def send_card_question(self):
        await self.players[self.turn].send_message("wat wilde doen met uw kaarten: %s" % START_OPTIONS)

    async def check_troel(self):
        for player in self.players:
            if player.count_aces() == 3:
                for team_player in self.players:
                    if team_player.count_aces() == 1:
                        await self.send_to(self.players, "den %s heeft 3 azen dus hij moet samen met %s" % (
                        player.name, team_player.name))
                        self.make_team([player, team_player])
                        return True
            if player.count_aces() == 4:
                heart_value = 13
                while True:
                    for team_player in self.players:
                        if team_player.has_card(Card(CardType.HARTEN, heart_value)) and team_player is not player:
                            await self.send_to(self.players,
                                               "den %s heeft 4 azen dus hij moet samen met %s" % (player.name,
                                                                                                  team_player.name))
                            self.make_team([player, team_player])
                            return True
                    heart_value -= 1
        return False

    def make_team(self, team_players: list):
        """
        makes a team of the given team_players and places the other players in the other team
        :param team_players: players in list form
        :return: nothing
        """
        leftover = copy.copy(self.players)
        for toremove in team_players:
            leftover.remove(toremove)
        self.teams = [team_players, leftover]

    @property
    def dealer(self):
        for player in self.players:
            if player.is_dealer:
                return player
        return None

    def get_wiezen_speler(self, identifier: str):
        for player in self.players:
            if player.identifier == identifier:
                return player
        return None

    def deal_cards(self):
        while len(self.card_deck.cards) != 0:
            for player in self.players:
                player.give_card(self.card_deck.get_card())

    async def show_cards(self):
        img_gen = ImageGenerator(1)
        for player in self.players:
            img_gen.hand_to_image(player)
            img_file = File(img_gen.get_output('hand').strip())
            await player.send_message("Hier zijn uwer kaarten")
            await player.send_message(img_file, is_file=True)

    async def send_to(self, players: list, message: str):
        for player in players:
            await player.send_message(message)
