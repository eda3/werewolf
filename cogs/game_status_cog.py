import asyncio
import random
import sys
from typing import List, TypeVar

from discord import Role, utils
from discord.channel import TextChannel
from discord.ext.commands import Bot, Cog, Context, command

from cogs.utils.const import GameStatusConst, join_channel_const
from cogs.utils.gamerole import GameRole
from cogs.utils.player import Player
from cogs.utils.roles import simple
from cogs.utils.werewolf_bot import WerewolfBot
from setup_logger import setup_logger

logger = setup_logger(__name__)


class GameStatusCog(Cog):
    def __init__(self, bot: WerewolfBot):
        logger.debug("GameStatusCogのinit")
        self.bot: WerewolfBot = bot

        # 参加者がリアクション絵文字を押した数
        self.react_num = 0

        # 参加者がリアクション絵文字を押した数
        self.react_num = 0

        # 議論時間
        self.discussion_time = 10

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
        """人狼ゲーム開始"""
        # メソッド名取得
        method: str = sys._getframe().f_code.co_name

        if self.bot.game.status == GameStatusConst.NOTHING.value:
            await ctx.send(f"まだ募集されておりません。{method}コマンドは使えません")
            return

        self.bot.game.status = GameStatusConst.PLAYING.value
        await ctx.send(f"ゲームのステータスを{self.bot.game.status}に変更しました")

        # 参加者に役職と鍵チャンネル権限設定
        await self.set_game_role(ctx)

        # ロールごとのアクション実行
        await self.role_action_exec(ctx)

        # wait_for()処理が終わった後に実行される
        await asyncio.sleep(1)
        await ctx.send("**5秒後に人狼ゲームを開始します。**")
        await asyncio.sleep(5)
        await ctx.send("**ゲーム開始です。それぞれの役職は自分にあった行動をしてください**")
        await asyncio.sleep(1)
        await ctx.send(f"**議論時間は{self.discussion_time}秒です**")
        await asyncio.sleep(self.discussion_time)
        await ctx.send("**(デバッグモード)ゲーム終了です**")
        # デバッグ用
        for p in self.bot.game.player_list:
            await ctx.send(f"{p.name}の役職は{p.after_game_role.name}でした")

    async def set_game_role(self, ctx: Context) -> None:
        # 役職配布
        n: int = len(self.bot.game.player_list)
        role_class_list = random.sample(simple[n], n)
        role_list: List[GameRole] = []
        for role in role_class_list:
            role_list.append(role(self.bot))

        # 鍵チャンネルへの権限を設定
        await self.set_channel_role(ctx)

        # 各参加者にゲーム役職を追加
        for i, player in enumerate(self.bot.game.player_list):
            name: str = player.name
            role = role_list[i]

            # 送信先チャンネル取得
            channel_name: str = "join0" + str(i)
            channel: TextChannel = ctx.guild.get_channel(join_channel_const[i])
            await channel.send(f"{channel_name}に送信。{name}の役職は{role.name}です")

            # 各Playerのプロパティに情報設定
            player.channel = channel
            player.game_role = role
            # 怪盗に交換された後のゲームロール
            player.after_game_role = role

    async def role_action_exec(self, ctx: Context) -> None:
        role_action_list = []
        for player in self.bot.game.player_list:
            # wait_for()含む処理を並列に動かすため、各役職のアクションメソッドをリストに入れる
            role_action_list.append(
                asyncio.create_task(player.game_role.action(player, player.channel))
            )

        # リアクションチェック用
        role_action_list.append(asyncio.create_task((self.check_react(ctx))))

        # weit_for()を含むrole_action()を並列実行
        for role_action in role_action_list:
            num = await role_action
            self.react_num += num

    async def check_react(self, ctx: Context) -> int:
        # リアクション数がプレイヤ数より下回ってる場合催促する
        while self.react_num < len(self.bot.game.player_list):
            remaining_num = len(self.bot.game.player_list) - self.react_num
            await ctx.send(f"{remaining_num}人がまだリアクション絵文字を押してないです")
            await asyncio.sleep(15)
        await ctx.send("**全員がリアクション絵文字を押したのを確認しました**")

        # self.check_numの加算でエラーにしなようにするため
        return 0

    async def set_channel_role(self, ctx: Context) -> None:
        player_list: List[Player] = self.bot.game.player_list
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
