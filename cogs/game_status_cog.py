import random
import sys
from typing import List

from discord import Role, utils
from discord.ext.commands import Bot, Cog, Context, command

from cogs.utils.const import GameStatusConst, join_channel_const
from cogs.utils.roles import simple
from cogs.utils.werewolf_bot import WerewolfBot
from setup_logger import setup_logger

logger = setup_logger(__name__)


class GameStatusCog(Cog):
    def __init__(self, bot: WerewolfBot):
        logger.debug("GameStatusCogのinit")
        self.bot: WerewolfBot = bot

    @command(aliases=["cre"])
    async def create(self, ctx: Context) -> None:
        """人狼ゲーム作成(エイリアス[cre])"""
        if self.bot.game.status == GameStatusConst.PLAYING.value:
            await ctx.send("現在ゲーム中です。createコマンドは使えません")
            return
        if self.bot.game.status == GameStatusConst.WAITING.value:
            await ctx.send("現在参加者募集中です")
            return

        self.bot.game.status = GameStatusConst.WAITING.value
        await ctx.send("参加者の募集を開始しました。")

    @command()
    async def start(self, ctx: Context) -> None:
        """人狼ゲーム開始"""
        # メソッド名取得
        method: str = sys._getframe().f_code.co_name

        if self.bot.game.status == GameStatusConst.NOTHING.value:
            await ctx.send(f"まだ募集されておりません。{method}コマンドは使えません")
            return

        self.bot.game.status = GameStatusConst.PLAYING.value
        await ctx.send(f"ゲームのステータスを{self.bot.game.status}に変更しました")

        # 役職配布
        n: int = len(self.bot.game.player_list)
        role: str = simple[n]
        role_list: list[str] = random.sample(role, n)

        for i, player in enumerate(self.bot.game.player_list):
            name: str = player.name
            role: str = role_list[i]

            # 送信先チャンネル取得
            channel: Channel = ctx.guild.get_channel(join_channel_const[i])
            await channel.send(f"{name}の役職は{role}です")

        await self.set_game_role(ctx)

    async def set_game_role(self, ctx: Context) -> None:
        player_list: list[Player] = self.bot.game.player_list
        n: int = len(player_list)
        if 0 == n:
            await ctx.send("参加者は0人です")
            return

        for i, player in enumerate(player_list):
            d_role_name: str = "join0" + str(i)
            d_role: Role = utils.get(ctx.guild.roles, name=d_role_name)

            await player.d_member.add_roles(d_role)
            s: str = f"{player.name}さんは鍵チャンネル{d_role_name}にアクセス出来るようになりました"
            await ctx.send(s)

    @command(aliases=["sgs"])
    async def show_game_status(self, ctx: Context) -> None:
        """コマンド:現在のゲームステータスを表示

        :param ctx:
        :return:
        """
        await ctx.send("show_game_statusコマンドが実行されました")
        status: str = self.bot.game.status
        await ctx.send(f"現在のゲームのステータスは{status}です")

    @command(aliases=["setgs"])
    async def set_game_status(self, ctx: Context, status: str = "") -> None:
        """コマンド：ゲームステータスを引数statusに設定

        :param ctx:
        :param status:ゲームのステータス。GameStatusConst参照
        :return:
        """
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
