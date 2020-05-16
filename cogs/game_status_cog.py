from discord.ext.commands import Bot, Cog, command, context

from cogs.utils.const import GameStatus
from setup_logger import setup_logger
from Typing import List

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

    @command(aliases=["setgs"])
    async def set_game_status(self, ctx: context, status: str = "") -> None:
        status_list: List[str] = [x.value for x in GameStatus]

        if status == "":
            await ctx.send(f"引数がありません。引数は以下からえらんでください。 {status_list}")
            return

        if status not in status_list:
            await ctx.send(f"引数が間違っています。引数は以下からえらんでください。{status_list}")
            return

        await ctx.send(f"あなたが選んだ引数は{status}です")


def setup(bot: Bot) -> None:
    bot.add_cog(GameStatusCog(bot))
