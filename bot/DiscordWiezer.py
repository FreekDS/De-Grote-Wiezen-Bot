from concurrent.futures import ThreadPoolExecutor

from wiezenlibrary.Player import Player

_executor = ThreadPoolExecutor(10)


class DiscordWiezer(Player):
    """
    implementation of the abstract Player class for the discord api
    """

    def __init__(self, discord_member, is_dealer: bool):
        super(DiscordWiezer, self).__init__(discord_member.name, str(discord_member.id), is_dealer)
        self.discord_member = discord_member

    async def send_message(self, message, is_file=False):
        if is_file:
            return await self.discord_member.send(file=message)
        else:
            return await self.discord_member.send(message)
