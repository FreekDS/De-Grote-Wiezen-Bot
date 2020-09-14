import asyncio

from discord import Message, File

from CliPlayer import CliPlayer
from wiezenlibrary.Game import Game


class CliWiezen(Game):

    def __init__(self, parent):
        self.stop_notifier = parent
        super().__init__()

    def stop(self):
        self.stop_notifier.stop(self)

    def update_table_images(self):
        msg: Message
        self.send_tables()

    def show_cards(self, players: list):
        for player in players:
            cardString = ""
            for idx, card in enumerate(player.hand):
                cardString += str(idx + 1) + ": " + str(card) + ", "
            print(player.name + ": " + cardString)

    def send_to(self, players: list, message: str or File, img=False):
        for player in players:
            if img:
                print("?")
            else:
                player.send_message(message)


if __name__ == '__main__':
    playerslist = list()
    game = CliWiezen(None)
    game.add_player(CliPlayer("1", True))
    game.add_player(CliPlayer("2", False))
    game.add_player(CliPlayer("3", False))
    game.add_player(CliPlayer("4", False))
    playerslist = game.players
    game.start_game()
    while True:
        message = input()
        player = int(message[0])
        action = message[2:]

        game.perform_action(playerslist[player - 1], action)
