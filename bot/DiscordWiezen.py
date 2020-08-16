from wiezenlibrary.Game import Game
class DiscordWiezen(Game):

    def __init__(self, bot, parent):
        self.stop_notifier=parent
        super().__init__(bot)

    async def stop(self):
        self.stop_notifier.stop(self)