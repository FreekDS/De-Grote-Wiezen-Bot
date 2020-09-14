import abc
import asyncio
import copy
import enum
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List, Dict

from discord import File, Message

from wiezenlibrary.Card import Card
from wiezenlibrary.Card import CardType
from wiezenlibrary.Deck import Deck
from wiezenlibrary.Player import Player
from wiezenlibrary.Slag import Slag
from wiezenlibrary.Team import Team
from wiezenlibrary.strategies.AbstractStrategy import AbstractStrategy
from wiezenlibrary.strategies.AskStrategy import AskStrategy
from wiezenlibrary.strategies.DansenAloneStrategy import DansenAloneStrategy
from wiezenlibrary.strategies.MiserieAloneStrategy import MiserieAloneStrategy
from wiezenlibrary.strategies.SoloAloneStrategy import SoloAloneStrategy
from wiezenlibrary.strategies.TroelAcesStrategy import TroelAcesStrategy

_executor = ThreadPoolExecutor(10)


class GameState(enum.Enum):
    DEALING = 0
    START = 1
    PLAYING = 2
    END = 3


# Other game options: TROEL <= gets triggered when someone has 3 aces
START_OPTIONS = ["Vraag", "Pas", "Dansen", "Solo", "Miserie"]


class Game():
    def __init__(self):
        self.card_deck = Deck()
        self.teams = list()
        self.players: List[Player] = []
        self.table: List[Card] = []
        self.troef = None
        self.current_slag: Slag or None = None
        self.slag_count = 0
        self.state = None
        self.turn = None
        self.answered = None
        self.change_troef_player = None
        self.first_troef_play = None
        self.start_normal = True

        # UI Related
        self.table_messages: Dict[Player or str, Message or None] = dict()

    ##### pre setup functions #####
    def set_spectator_message(self, message: Message):
        self.table_messages["SPECTATOR"] = message

    def set_player_table_message(self, player: Player, message: Message):
        if player not in self.table_messages.keys():
            return False
        self.table_messages[player] = message

    def add_player(self, player: Player):
        dealer = player.is_dealer and not self.dealer  # make sure to only have one dealer
        self.players.append(player)
        self.table_messages[player] = None

    ##### main action function#####
    def perform_action(self, player, action):
        if self.state == GameState.DEALING:
            self.handle_dealer_answer(action, player)
        elif self.state == GameState.START:
            self.handle_question(player, action)
        elif self.state == GameState.PLAYING:
            self.handle_gameplay_message(player, action)
        elif self.state == GameState.END:
            self.handle_end_game_answer(player, action)

    ##### dealer mode function #####
    def start_game(self):
        self.state = GameState.DEALING
        self.dealer.ask_shuffles()

    def handle_dealer_answer(self, action, player):
        if player.is_dealer:
            try:
                if (int(action) > 10000):
                    self.send_to([player],
                                 "das misschien wat te veel van het goede, pakt dat we met 1 keer beginnen")
                    action = "1"
                self.card_deck.shuffle(int(action))
            except Exception as e:
                self.send_to([player], "ok dat was grappig, maar nu moogt ge wel eens een geldig nummer geven.")
                return
            player.send_message("ge hebt %s keer geshoumeld" % action)

            self.deal_cards()
            self.show_cards(self.players)
            self.start_questions()
        else:
            self.send_to((player), "mateke wacht eens op den dealer")

    ##### start mode functions #####
    def start_questions(self):
        self.state = GameState.START
        if self.check_troel():
            self.start_rounds()
        else:
            self.turn = 0
            self.send_card_question()

    def send_card_question(self):
        self.players[self.turn].send_message(
            "wat wilde doen met uw kaarten: %s" % START_OPTIONS)

    def handle_question(self, player, action):
        if self.change_troef_player is not None:
            self.change_troef(action, player)
            return

        if self.answered is not None:
            if self.players[(self.turn + len(self.answered) + 1)%4].identifier != player.identifier:
                self.send_to([player], "Elaba stopt eens met onze bot kapot te maken")
                return
            if action == "nee":
                self.handle_no_answer(player)
            elif action == "ja":
                self.handle_Yes_answer(player)
        else:
            if self.players[self.turn].identifier != player.identifier:
                self.send_to([player], "Elaba stopt eens met onze bot kapot te maken")
                return
            if action == "Vraag":
                self.handle_vraag_answer()
            elif action == "Pas":
                self.handle_pas_answer(player)
            elif action == "Dansen":
                self.handle_dansen_answer(player)
            elif action == "Solo":
                self.handle_solo_answer(player)
            elif action == "Miserie":
                self.handle_miserie_answer(player)

    def change_troef(self, action, player):
        if player.identifier == self.change_troef_player.identifier:
            if action == "harten":
                self.troef = CardType.HARTEN
            elif action == "schoppen":
                self.troef = CardType.SCHOPPEN
            elif action == "koeken":
                self.troef = CardType.KOEKEN
            elif action == "klaveren":
                self.troef = CardType.KLAVEREN
            else:
                self.send_to([player], "da verstaank nie")
                return
            self.send_to(self.players, "vanaf nu is %s troef" % action)
            self.change_troef_player = None
            self.start_rounds()

    def handle_solo_answer(self, player):
        self.send_to(self.players, "den %s gaat solo" % player.name)
        self.make_team([player], SoloAloneStrategy())
        self.send_to([player], "welk wilt ge als troef? [harten,schoppen,koeken,klaveren]")
        self.reorder_players(self.players.index(player))
        self.set_start_override_false()
        player.start_override = True
        self.change_troef_player = player

    def handle_dansen_answer(self, player):
        self.send_to(self.players, "den %s gaat een danske placeren en wilt 9 troeven halen" % player.name)
        self.make_team([player], DansenAloneStrategy())
        self.send_to([player], "welk wilt ge als troef? [harten,schoppen,koeken,klaveren]")
        self.reorder_players(self.players.index(player))
        self.set_start_override_false()
        player.start_override = True
        self.change_troef_player = player

    def handle_miserie_answer(self, player):
        self.send_to(self.players, "den %s heeft veel miserie" % player.name)
        self.make_team([player], MiserieAloneStrategy())
        self.send_to(self.players, "vanaf nu is er geen troef niet meer, sad!")
        self.reorder_players(self.players.index(player))
        self.troef = None
        self.set_start_override_false()
        player.start_override = True
        self.start_rounds()

    def handle_pas_answer(self, player):
        self.send_to(self.players, "den %s zegt dat hem moet passen van zijn moeder" % player.name)
        self.advance_question_turn()


    def handle_vraag_answer(self):
        self.answered = list()
        self.players[(self.turn + len(self.answered) + 1)%4].send_message(
            "den %s vraagt, wilt ge mee? ja/nee" %
            self.players[self.turn].name)

    def handle_Yes_answer(self, player):
        self.send_to(self.players,
                     "%s heeft een coalitie gemaakt met %s" %
                     (self.players[self.turn].name, player.name))
        self.make_team([self.players[self.turn], player], AskStrategy())
        self.start_rounds()

    def handle_no_answer(self, player):
        self.answered.append(player)
        if len(self.answered) == 3:
            self.send_to(self.players, "niemand wilt mee met den %s, sad" % self.players[self.turn].name)
            self.advance_question_turn()
            self.answered = None
            self.send_card_question()
        else:
            self.players[(self.turn + len(self.answered) + 1)%4].send_message(
                    "den %s vraagt, wilt ge mee? ja/nee" %
                    self.players[self.turn].name)

    def check_troel(self):
        for player in self.players:
            if player.count_aces() == 3:
                for idx, team_player in enumerate(self.players):
                    if team_player.count_aces() == 1:
                        self.troef = team_player.get_aces()[0].type
                        self.first_troef_play = team_player.get_aces()[0]
                        self.send_to(self.players,
                                     "den %s heeft 3 azen dus hij moet samen met %s en den %s is troef nu" % (
                                         player.name, team_player.name, CardType.get_name(self.troef)))
                        self.make_team([player, team_player], TroelAcesStrategy())
                        self.set_start_override_false()
                        team_player.start_override = True
                        self.reorder_players(idx)
                        return True
            if player.count_aces() == 4:
                heart_value = 13
                while True:
                    for idx, team_player in enumerate(self.players):
                        if team_player.has_card(Card(CardType.HARTEN, heart_value)) and team_player is not player:
                            self.first_troef_play = Card(CardType.HARTEN, heart_value)
                            self.troef = player.get_aces()[3].type
                            self.send_to(self.players,
                                         "den %s heeft 4 azen dus hij moet samen met %s en %s is troef nu" % (
                                             player.name,
                                             team_player.name, CardType.get_name(self.troef)))

                            self.make_team([player, team_player], TroelAcesStrategy())
                            self.set_start_override_false()
                            team_player.start_override = True
                            self.reorder_players(idx)
                            return True
                    heart_value -= 1
        return False

    def set_start_override_false(self):
        self.start_normal = False
        for player in self.players:
            player.start_override = False

    def set_start_override_None(self):
        self.start_normal = True
        for player in self.players:
            player.start_override = None

    def advance_question_turn(self):
        self.turn += 1
        if self.turn > 3:
            if self.state == GameState.START:
                self.send_to(self.players, "allé dat we niet willen spelen dan beginnen we maar opnieuw hé")
                self.state = GameState.DEALING
                self.card_deck= Deck()
                self.turn = 0
                self.dealer.ask_shuffles()
                return
            else:
                self.turn = 0
        self.send_card_question()

    def make_team(self, team_players: list, strategy: AbstractStrategy):
        """
        makes a team of the given team_players and places the other players in the other team
        :param team_players: players in list form
        :return: nothing
        """
        leftover = copy.copy(self.players)
        for toremove in team_players:
            leftover.remove(toremove)

        self.teams = [Team(team_players, strategy), Team(leftover, strategy.get_oposite())]

    def reorder_players(self, idx):
        """
        Function that places the player at idx to the front of the array while keeping the array order
        :param idx: the idx of the player
        :return: nothing
        """
        newlist = self.players[idx:]
        newlist += self.players[:idx]
        self.players = newlist

    ##### round functions #####
    def start_rounds(self):
        self.state = GameState.PLAYING
        for idx, player in enumerate(self.players):
            if player.must_start:
                if self.start_normal:
                    self.reorder_players(idx)
                self.set_start_override_None()
                self.turn = 0
                self.start_new_slag()
                self.current_slag.first = True
                self.send_tables()
                self.send_to(self.players, "den %s mag beginnen" % self.players[0].name)
                self.show_cards([self.players[0]])
                self.send_to([self.players[0]], "welke kaardt wilde leggen?")
                break

    def handle_gameplay_message(self, player, action):
        if self.players[self.turn].identifier != player.identifier:
            self.send_to([player], "Wacht eens op uw beurt maneke")
            return
        # FIXME zet dit terug aan opt einde
        # try:
        card_index = int(action) - 1
        chosen_card = self.players[self.turn].get_card(card_index)
        if self.check_allowed(player, chosen_card):
            self.players[self.turn].remove_card(card_index)
            self.send_to(self.players, "den %s legt een %s" % (player.name, chosen_card))
            self.current_slag.lay_card(player, chosen_card)
            self.update_table_images()
            self.advance_gameplay_turn()
        # except Exception as e:
        #     self.send_to([player], "Geeft eens een geldige kaart man")

    def check_allowed(self, player, card):
        # You can't lay a troef in the first slag unless when doing troel
        if self.current_slag.first:
            if self.troef != None and card.type == self.troef and self.first_troef_play == None:
                self.send_to([player], "mateke ge geen troef leggen in den eerste slag")
                return False
            if self.first_troef_play != None and self.first_troef_play != card:
                self.send_to([player],
                             "mateke ge zijt troel gegaan, nu moet ge de kaart leggen waardoor ge troel zijt (aas of hoogste harten)")
                self.current_slag.first = False
                return False

        # First card in a slag that is being laid
        if self.current_slag.type is None: return True

        if player.has_type(self.current_slag.type):
            if card.type != self.current_slag.type:
                self.send_to([player],
                             "seg gij kunt nog een kaart leggen dat overeen komt met het type van de slag, doe dat eens")
                return False
        return True

    def advance_gameplay_turn(self):
        self.turn += 1
        if self.turn > 3:
            winner = self.current_slag.check_winner()
            self.send_to(self.players,
                         "den %s wint de slag met een %s" %
                         (winner[0].name, str(winner[1])))
            winner[0].round_wins += 1
            self.reorder_players(self.players.index(winner[0]))
            if self.check_team_wins():
                self.start_end_game()
                self.turn = 0
                return

            self.start_new_slag()
            self.send_tables()
            self.turn = 0

        self.show_cards([self.players[self.turn]])
        self.send_to([self.players[self.turn]], "welke kaardt wilde leggen?")

    def start_new_slag(self):
        self.current_slag = Slag(self.troef)
        self.slag_count += 1
        self.send_to(self.players, "<>===== Start Slag %s =====<>" % (self.slag_count))

    def check_team_wins(self):
        if self.teams[0].check_team_win(self.teams[1]):
            self.send_to(self.players, "gohoho het team van %s is gewonnen" % (str(self.teams[0])))
            self.teams[0].give_points()
            return True
        if self.teams[1].check_team_win(self.teams[0]):
            self.send_to(self.players, "gohoho het team van %s is gewonnen" % (str(self.teams[1])))
            self.teams[1].give_points()
            return True
        return False

    ##### End game question + restart #####

    def start_end_game(self):
        self.state = GameState.END
        self.print_current_scores()
        self.answered = list()
        self.send_to(self.players, "doen we der nog eentje? [ja, nee]")

    def handle_end_game_answer(self, player, action):
        if (action == 'ja'):
            self.send_to(self.players, "nog ne keer? ok!")
            self.cleanup_for_start()
            self.start_game()

        elif (action == "nee"):
            self.send_to(self.players, "ok, dan stoppen we dermee")
            self.stop()

    @abc.abstractmethod
    def stop(self):
        pass

    def cleanup_for_start(self):
        self.card_deck = Deck()
        self.teams = list()
        self.table: List[Card] = []
        self.troef = None
        self.current_slag: Slag or None = None
        self.slag_count = 0
        self.state = None
        self.turn = None
        self.answered = None
        self.change_troef_player = None
        self.first_troef_play = None
        self.start_normal = True

    def print_current_scores(self):
        players = copy.copy(self.players)
        players.sort(reverse=True, key=lambda player: player.total_points)
        self.send_to(self.players, "score bord")
        place = 1
        prev_score = None
        for player in players:
            if (prev_score != None and player.total_points != prev_score):
                place += 1
            self.send_to(self.players, "%s: %s met %s punten" % (place, player.name, player.total_points))
            prev_score = player.total_points

    ##### UI and util functions #####
    @abc.abstractmethod
    def send_tables(self):
        pass

    @property
    def dealer(self):
        for player in self.players:
            if player.is_dealer:
                return player
        return None

    def get_wiezen_speler(self, identifier: str, override=None):
        if (override):
            return self.players[override]
        for player in self.players:
            if player.identifier == identifier:
                return player
        return None

    def deal_cards(self):
        last_card = None
        while len(self.card_deck.cards) != 0:
            for player in self.players:
                last_card = self.card_deck.get_card()
                player.give_card(last_card)
        self.troef = last_card.type
        self.send_to(self.players, "%s is (s)troef" % CardType.get_name(self.troef))

    @abc.abstractmethod
    def show_cards(self, players: list):
        pass

    @abc.abstractmethod
    def send_to(self, players: list, message: str or File, img=False):
        pass

    @abc.abstractmethod
    def update_table_images(self):
        pass