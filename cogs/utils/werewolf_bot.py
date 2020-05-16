from discord.ext.commands import Bot

from cogs.utils.game import Game


class WerewolfBot(Bot):
    game: Game

