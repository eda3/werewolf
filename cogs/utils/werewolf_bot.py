from discord.ext.commands import Bot

from cogs.utils.game import Game


class WerewolfBot(Bot):

    def __init__(self, game: Game):
        super().__init__(command_prefix=";")
        self.game = game

