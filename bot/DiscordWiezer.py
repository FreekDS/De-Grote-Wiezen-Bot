from wiezenlibrary.Player import Player
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(10)

class DiscordWiezer(Player):
    """
    implementation of the abstract Player class for the discord api
    """

    def __init__(self, discord_member, is_dealer: bool):
        super(DiscordWiezer, self).__init__(discord_member.name, str(discord_member.id), is_dealer)
        self.discord_member = discord_member

    def send_message(self, message, is_file=False):
        # print("adding message")
        # self.messages.append((message,is_file))
        loop = asyncio.get_event_loop()
        if is_file:
            asyncio.run_coroutine_threadsafe(self.discord_member.send(file=message), loop)
        else:
            asyncio.run_coroutine_threadsafe(self.discord_member.send(message), loop)