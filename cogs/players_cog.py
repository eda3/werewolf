import sys

from discord.ext.commands import Bot, Cog, command, context
from discord.member import Member

from cogs.utils.const import GameStatusConst
from cogs.utils.player import Player
from cogs.utils.werewolf_bot import WerewolfBot
from setup_logger import setup_logger

logger = setup_logger(__name__)


class PlayersCog(Cog):
    def __init__(self, bot: WerewolfBot):
        self.bot: WerewolfBot = bot

    @command()
    async def join(self, ctx: context) -> None:
        # メソッド名取得
        method: str = sys._getframe().f_code.co_name

        member: Member = ctx.author
        if self.bot.game.status == GameStatusConst.NOTHING.value:
            await ctx.send(f"現在募集していません。{method}コマンドは使えません")
            return
        if self.bot.game.status == GameStatusConst.PLAYING.value:
            await ctx.send(f"現在ゲーム進行中です。{method}コマンドは使えません")
            return

        player: Player = Player(member.id)
        self.bot.game.join_player(player)
        await ctx.send(f"{member}がjoinしました")
        for p in self.bot.game.player_list:
            logger.debug(f"{p=}")


def setup(bot: Bot) -> None:
    bot.add_cog(PlayersCog(bot))
