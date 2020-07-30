import copy
from pydoc import plain

from discord import File

from ImageGenerator import ImageGenerator
from wiezenlibrary.Deck import Deck
from typing import List
from wiezenlibrary.Player import Player
from wiezenlibrary.Card import Card
import enum

from wiezenlibrary.Card import CardType
from wiezenlibrary.Team import Team, PLAYER_STRATS

from Slag import Slag


class GameState(enum.Enum):
    DEALING = 0
    START = 1
    PLAYING = 2
    END = 3


# Other game options: TROEL <= gets triggered when someone has 3 aces
START_OPTIONS = ["Vraag", "Pas", "Dansen", "Solo", "Miserie"]


class Game:
    def __init__(self):
        self.card_deck = Deck()
        self.teams = list()
        self.players: List[Player] = []
        self.table: List[Card] = []
        self.troef = None
        self.current_slag = None
        self.state = None
        self.turn = None
        self.answered = None

    def add_player(self, player: Player):
        dealer = player.is_dealer and not self.dealer  # make sure to only have one dealer
        self.players.append(player)

    async def perform_action(self, player, action):
        if self.state == GameState.DEALING:
            await self.handle_dealer_answer(action, player)
        elif self.state == GameState.START:
            await self.handle_question(player, action)
        elif self.state == GameState.PLAYING:
            await self.handle_gameplay_message(player, action)

    async def handle_dealer_answer(self, action, player):
        if player.is_dealer:
            self.card_deck.shuffle(int(action))
            await player.send_message("ge hebt %s keer geshoumeld" % action)
            await self.deal_cards()
            await self.show_cards(self.players)
            await self.start_questions()
        else:
            await player.discord_member.send("mateke wacht eens op den dealer")

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
            elif action == "Dansen":
                await self.handle_dansen_answer(player)
            elif action == "Solo":
                await self.handle_solo_answer(player)
            elif action == "Miserie":
                await self.handle_miserie_answer(player)

    async def handle_solo_answer(self, player):
        await self.send_to(self.players, "den %s gaat solo" % player.name)
        self.make_team([player],PLAYER_STRATS.SOLOSOLO)
        await self.start_rounds()

    async def handle_dansen_answer(self, player):
        await self.send_to(self.players, "den %s gaat een danske placeren en wilt 9 troeven halen" % player.name)
        self.make_team([player], PLAYER_STRATS.DANSENALONE)
        await self.start_rounds()

    async def handle_miserie_answer(self, player):
        await self.send_to(self.players, "den %s heeft veel miserie" % player.name)
        self.make_team([player], PLAYER_STRATS.MISERIEAlONE)
        await self.start_rounds()

    async def handle_pas_answer(self, player):
        await self.send_to(self.players, "den %s zegt dat hem moet passen van zijn moeder" % player.name)
        await self.advance_question_turn()
        await self.send_card_question()

    async def handle_vraag_answer(self):
        self.answered = list()
        await self.players[self.turn + len(self.answered) + 1].send_message(
            "den %s vraagt, wilt ge mee? ja/nee" %
            self.players[self.turn].name)
        await self.advance_question_turn()

    async def handle_Yes_answer(self, player):

        await self.send_to(self.players,
                           "%s heeft een coalitie gemaakt met %s" %
                           (self.players[self.turn].name, player.name))
        self.make_team([self.players[self.turn], player], PLAYER_STRATS.SAAI)
        await self.start_rounds()

    async def handle_no_answer(self, player):
        self.answered.append(player)
        if len(self.answered) == 3 - self.turn:
            await self.send_to(self.players, "niemand wilt mee met den %s, sad" % self.players[self.turn].name)
            await self.advance_question_turn()
            self.answered = None
            await self.send_card_question()
        else:
            await self.players[self.turn + len(self.answered) + 1].send_message(
                "den %s vraagt, wilt ge mee? ja/nee" %
                self.players[self.turn].name)

    async def advance_question_turn(self):
        self.turn += 1
        if self.turn > 3:
            if self.state.state == GameState.START:
                await self.send_to(self.players, "allé dat we niet willen spelen dan beginnen we maar opnieuw hé")
                self.state = GameState.DEALING
                self.turn = 0
                await self.dealer.ask_shuffles()
            else:
                self.turn = 0

    async def start_game(self):
        self.state = GameState.DEALING
        await self.dealer.ask_shuffles()

    async def start_questions(self):
        self.state = GameState.START
        if await self.check_troel():
            await self.start_rounds()
        else:
            self.turn = 0
            await self.send_card_question()

    async def start_rounds(self):
        self.state = GameState.PLAYING
        for idx, player in enumerate(self.players):
            if player.must_start:
                self.reorder_players(idx)
                self.turn = 0
                await self.send_to(self.players, "den %s mag beginnen" % self.players[0].name)
                await self.show_cards([self.players[0]])
                await self.send_to([self.players[0]], "welke kaardt wilde leggen?")
                self.current_slag = Slag(self.troef)
                break

    def reorder_players(self, idx):
        """
        Function that places the player at idx to the front of the array while keeping the array order
        :param idx: the idx of the player
        :return: nothing
        """
        newlist = self.players[idx:]
        newlist += self.players[:idx]
        self.players = newlist

    async def handle_gameplay_message(self, player, action):
        if  self.players[self.turn].identifier!=player.identifier:
            await self.send_to([player], "Wacht eens op uw beurt maneke")
            return
        # FIXME zet dit terug aan opt einde
        # try:
        card_index = int(action) - 1
        chosen_card = self.players[self.turn].get_card(card_index)
        await self.send_to(self.players, "den %s legt een %s" % (player.name, chosen_card))
        self.current_slag.lay_card(player, chosen_card)
        await self.advance_gameplay_turn()
        # except Exception as e:
        #     await self.send_to([player], "Geeft eens een geldige kaart man")


    # TODO een goeie check functie maken
    def check_allowed(self, player, card):
        return True

    async def advance_gameplay_turn(self):
        self.turn += 1
        if (self.turn > 3):
            winner=self.current_slag.check_winner()
            await self.send_to(self.players,
                               "den %s wint de slag met een %s" %
                               (winner[0].name,str(winner[1])))
            winner[0].round_wins+=1
            self.reorder_players(self.players.index(winner[0]))
            if(self.teams[0].check_team_win(self.teams[1])):
                await self.send_to(self.players,"gohoho het team van %s is gewonnen"%(str(self.teams[0])))
                self.reset()
                return
            if (self.teams[1].check_team_win(self.teams[0])):
                await self.send_to(self.players, "gohoho het team van %s is gewonnen" % (str(self.teams[1])))
                self.reset()
                return
            self.turn=0

        await self.show_cards([self.players[self.turn]])
        await self.send_to([self.players[self.turn]], "welke kaardt wilde leggen?")



    async def send_card_question(self):
        await self.players[self.turn].send_message("wat wilde doen met uw kaarten: %s" % START_OPTIONS)

    async def check_troel(self):
        for player in self.players:
            if player.count_aces() == 3:
                for team_player in self.players:
                    if team_player.count_aces() == 1:
                        self.troef = team_player.get_aces()[0].type
                        await self.send_to(self.players,
                                           "den %s heeft 3 azen dus hij moet samen met %s en den %s is troef nu" % (
                                               player.name, team_player.name,CardType.get_name(self.troef)))
                        self.make_team([player, team_player], PLAYER_STRATS.TROELMETAZEN)
                        return True
            if player.count_aces() == 4:
                heart_value = 13
                while True:
                    for team_player in self.players:
                        if team_player.has_card(Card(CardType.HARTEN, heart_value)) and team_player is not player:
                            self.troef = player.get_aces()[3].type
                            await self.send_to(self.players,
                                               "den %s heeft 4 azen dus hij moet samen met %s en %s is troef nu" % (
                                                   player.name,
                                                   team_player.name, CardType.get_name(self.troef)))
                            self.make_team([player, team_player], PLAYER_STRATS.TROELMETAZEN)
                            return True
                    heart_value -= 1
        return False

    def make_team(self, team_players: list, strategy: PLAYER_STRATS):
        """
        makes a team of the given team_players and places the other players in the other team
        :param team_players: players in list form
        :return: nothing
        """
        leftover = copy.copy(self.players)
        for toremove in team_players:
            leftover.remove(toremove)

        self.teams = [Team(team_players, strategy), Team(leftover, PLAYER_STRATS.get_oposite(strategy))]

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

    async def deal_cards(self):
        last_card = None
        while len(self.card_deck.cards) != 0:
            for player in self.players:
                last_card = self.card_deck.get_card()
                player.give_card(last_card)
        self.troef = last_card.type
        await self.send_to(self.players, "%s is (s)troef" % CardType.get_name(self.troef))

    async def show_cards(self, players: list):
        img_gen = ImageGenerator(1)
        for player in players:
            img_gen.hand_to_image(player)
            img_file = File(img_gen.get_output('hand').strip())
            await player.send_message("Hier zijn uwer kaarten")
            await player.send_message(img_file, is_file=True)

    async def send_to(self, players: list, message: str):
        for player in players:
            await player.send_message(message)

    def reset(self):
        self.state = GameState.DEALING
        self.players.clear()
