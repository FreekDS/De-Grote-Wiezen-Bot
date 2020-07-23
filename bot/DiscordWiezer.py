from Player import Player


class DiscordWiezer(Player):
    """
    implementation of the abstract Player class for the discord api
    """
    def __init__(self, discord_member, is_dealer: bool):
        super(DiscordWiezer, self).__init__(discord_member.name,str(discord_member.id),is_dealer)
        self.discord_member = discord_member
    async def send_message(self,message):
        await self.discord_member.send(message)

