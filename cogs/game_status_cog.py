from discord.ext.commands import Bot, Cog, command, context

from cogs.utils.player import Player


from setup_logger import setup_logger

logger = setup_logger(__name__)


class GameStatusCog(Cog):
    def __init__(self, bot: Bot):
        logger.debug("GameStatusCogのinit")
        self.bot = bot

    @command(aliases=["sgs"])
    async def show_game_status(self, ctx: context) -> None:
        await ctx.send("show_game_statusコマンドが実行されました")
        status: str = self.bot.game.status.value
        await ctx.send(f"現在のゲームのステータスは{status}です")


def setup(bot: Bot) -> None:
    bot.add_cog(GameStatusCog(bot))
