from wiezenlibrary.Player import Player
from discord import File


class CliPlayer(Player):
    """
    implementation of the abstract Player class for the discord api
    """

    def __init__(self, name, is_dealer: bool):
        super(CliPlayer, self).__init__(name,name, is_dealer)

    def send_message(self, message, is_file=False):
        if is_file:
            print("huh ik mag toch geen files krijgen")
        else:
            print(self.name+": "+message)
