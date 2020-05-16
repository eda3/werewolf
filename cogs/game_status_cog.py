from discord.ext.commands import Bot, Cog, command, context

from cogs.utils.const import GameStatusConst
from setup_logger import setup_logger
from typing import List

logger = setup_logger(__name__)


class GameStatusCog(Cog):
    def __init__(self, bot: Bot):
        logger.debug("GameStatusCogのinit")
        self.bot = bot

    @command(aliases=["sgs"])
    async def show_game_status(self, ctx: context) -> None:
        await ctx.send("show_game_statusコマンドが実行されました")
        status: str = self.bot.game.status
        await ctx.send(f"現在のゲームのステータスは{status}です")

    @command(aliases=["setgs"])
    async def set_game_status(self, ctx: context, status: str = "") -> None:
        status_list: List[str] = [x.value for x in GameStatusConst]

        if status == "":
            await ctx.send(f"引数がありません。引数は以下からえらんでください。 {status_list}")
            return

        if status not in status_list:
            await ctx.send(f"引数が間違っています。引数は以下からえらんでください。{status_list}")
            return

        self.bot.game.status = status
        await ctx.send(f"ゲームのステータスを{status}にセットしました")


def setup(bot: Bot) -> None:
    bot.add_cog(GameStatusCog(bot))
