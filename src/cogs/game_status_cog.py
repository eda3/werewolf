from typing import List

from discord import Role, utils
from discord.ext.commands import Bot, Cog, Context, command

from cogs.utils.const import GameStatusConst, join_channel_const
from cogs.utils.werewolf_bot import WerewolfBot
from setup_logger import setup_logger

logger = setup_logger(__name__)


class GameStatusCog(Cog):
    def __init__(self, bot: WerewolfBot):
        logger.debug("GameStatusCogのinit")
        self.bot: WerewolfBot = bot

    @command(aliases=["cre", "c"])
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

    @command(aliases=["sta", "s"])
    async def start(self, ctx: Context) -> None:
        await self.bot.game.start(ctx)

    @command()
    async def end(self, ctx: Context) -> None:
        """人狼ゲーム終了"""

        # 秘匿チャンネルの役職解除
        await self.reset_discord_role(ctx)
        # 参加者一覧を削除
        self.bot.game.player_list.clear()

    @staticmethod
    async def reset_discord_role(ctx: Context) -> None:
        """秘匿チャンネルの役職解除

        :param ctx:
        :return:
        """
        for i in range(len(join_channel_const)):
            d_role_name: str = "join0" + str(i)
            d_role: Role = utils.get(ctx.guild.roles, name=d_role_name)
            for member in d_role.members:
                await member.remove_roles(d_role)

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
