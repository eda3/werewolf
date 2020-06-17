from discord.ext.commands import Bot

# from games.game import Game


class WerewolfBot(Bot):
    def __init__(self, game):
        super().__init__(command_prefix=";")
        self.game = game
