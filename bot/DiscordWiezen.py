import asyncio
from concurrent.futures import ThreadPoolExecutor
import nest_asyncio

from discord import Message, File

from ImageGenerator import ImageGenerator
from wiezenlibrary.Game import Game

_executor = ThreadPoolExecutor(10)
nest_asyncio.apply()

class DiscordWiezen(Game):
    def __init__(self, bot, parent):
        self.stop_notifier = parent
        super().__init__()

    def stop(self):
        self.stop_notifier.stop(self)

    def update_table_images(self):
        msg: Message
        for msg in self.table_messages.values():
            if msg:
                # loop = asyncio.get_event_loop()
                asyncio.ensure_future(
                    msg.delete()
                )
        self.send_tables()

    def show_cards(self, players: list):
        img_gen = ImageGenerator(1)
        for player in players:
            img_gen.hand_to_image(player)
            img_file = File(img_gen.get_output('hand').strip())
            # loop = asyncio.get_event_loop()
            asyncio.ensure_future(
                player.send_message("Hier zijn uwer kaarten")
            )
            asyncio.ensure_future(
                player.send_message(img_file, is_file=True))

    def send_to(self, players: list, message: str or File, img=False):
        for player in players:
            if img:
                file = File(message)
                # loop = asyncio.get_event_loop()
                asyncio.ensure_future(
                    self.sendMsg(file, player)
                )
            else:
                # loop = asyncio.get_event_loop()
                asyncio.ensure_future(
                    player.send_message(message)
                )

    async def sendMsg(self, file, player):
        msg = await player.send_message(file, is_file=True)
        self.table_messages[player] = msg

    def send_tables(self):
        ImageGenerator(1).generate_table(self.current_slag, self.players, self.teams)
        file = ImageGenerator(1).get_output('table').strip()
        self.send_to(self.players, file, img=True)
