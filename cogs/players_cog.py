import sys

from discord.ext.commands import Bot, Cog, Context, command
from discord.member import Member

from cogs.utils.const import GameStatusConst
from cogs.utils.player import Player
from cogs.utils.werewolf_bot import WerewolfBot
from setup_logger import setup_logger

logger = setup_logger(__name__)


class PlayersCog(Cog):
    def __init__(self, bot: WerewolfBot):
        self.bot: WerewolfBot = bot

    @command(aliases=["j"])
    async def join(self, ctx: Context) -> None:
        """ゲームに参加する。募集中のみ有効。

        :param ctx:
        :return:
        """
        # メソッド名取得
        method: str = sys._getframe().f_code.co_name

        member: Member = ctx.author
        if self.bot.game.status == GameStatusConst.NOTHING.value:
            await ctx.send(f"現在募集していません。{method}コマンドは使えません")
            return
        if self.bot.game.status == GameStatusConst.PLAYING.value:
            await ctx.send(f"現在ゲーム進行中です。{method}コマンドは使えません")
            return

        player: Player = Player(member)
        self.bot.game.join_player(player)
        await ctx.send(f"{member}がjoinしました")

    @command(aliases=["spl"])
    async def show_player_list(self, ctx: Context) -> None:
        """参加者一覧を表示

        :param ctx:
        :return:
        """
        p_list = [x for x in self.bot.game.player_list]
        pname_list = [x.name for x in p_list]
        await ctx.send(f"ゲームの参加者は{pname_list}です")


def setup(bot: Bot) -> None:
    bot.add_cog(PlayersCog(bot))
