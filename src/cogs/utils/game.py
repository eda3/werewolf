from __future__ import annotations

import asyncio
import random
import sys
from typing import List

from discord import Role, utils
from discord.ext.commands import Context

from cogs.utils.const import GameStatusConst, SideConst
from cogs.utils.player import Player
from cogs.utils.player_list import PlayerList
from cogs.utils.roles import simple
from setup_logger import setup_logger

logger = setup_logger(__name__)


class Game:
    def __init__(self) -> None:
        logger.debug("Gameクラス init")
        self.status = GameStatusConst.NOTHING.value
        self.player_list: PlayerList = PlayerList()

        # 参加者がリアクション絵文字を押した数
        self.react_num = 0

        # 議論時間
        # self.discussion_time = 300
        self.discussion_time = 1

        # 墓地送りになった役職
        self.grave_role_list = []

    async def start(self, ctx: Context) -> None:
        """人狼ゲーム開始"""
        # メソッド名取得
        method: str = sys._getframe().f_code.co_name

        if self.status == GameStatusConst.NOTHING.value:
            await ctx.send(f"まだ募集されておりません。{method}コマンドは使えません")
            return

        self.status = GameStatusConst.PLAYING.value
        await ctx.send(f"ゲームのステータスを{self.status}に変更しました")

        # 参加者に役職と鍵チャンネル権限設定
        role_name_list = await self.set_game_role(ctx)

        # ロールごとのアクション実行
        await self.role_action_exec(ctx)

        # wait_for()処理が終わった後に実行される
        await asyncio.sleep(1)
        await ctx.send("``` ```")
        await ctx.send("**5秒後に人狼ゲームを開始します。**")
        await asyncio.sleep(5)
        await ctx.send("**ゲーム開始です。それぞれの役職は自分にあった行動をしてください**")
        await asyncio.sleep(1)
        await ctx.send(f"**議論時間は{self.discussion_time}秒です**")
        await asyncio.sleep(1)
        await ctx.send(f"**__今回のゲームの役職は{role_name_list}です__**")

        # 30秒ごとに残り時間を出力
        while 0 < self.discussion_time:
            await asyncio.sleep(1)
            self.discussion_time = self.discussion_time - 1
            if self.discussion_time % 30 == 0:
                await ctx.send(f"**残り{self.discussion_time}秒です**")

        await ctx.send("**(デバッグモード)ゲーム終了です**")
        await asyncio.sleep(1)
        await ctx.send("**各自、投票を開始してください**")

        # ロールごとのアクション実行
        await self.vote_exec(ctx)
        await asyncio.sleep(1)
        await ctx.send("**投票が完了しました**")
        await asyncio.sleep(3)
        await ctx.send("**今回は……**")
        await asyncio.sleep(1)

        p_list = self.player_list
        # 平和村かどうか
        # 投票数が全員1かどうかをチェック
        if await self.is_vote_count_same_for_all(p_list):
            """投票された数が全員一緒のとき"""
            # プレイヤ内に人狼陣営がいるかチェック
            if await self.check_black_side_in_players(p_list):
                await ctx.send("**投票数全員1。人狼陣営が残っているため、**")
                await asyncio.sleep(1)
                await ctx.send("**__人狼陣営の勝利です！__**")
            else:
                await ctx.send("**投票数全員1。人狼陣営は残っていないため**")
                await asyncio.sleep(1)
                await ctx.send("**真の平和村でした**")
                await asyncio.sleep(1)
                await ctx.send("**__全員の勝利です！__**")
        else:
            """投票で誰かが選ばれたとき"""
            # 一番投票されたプレイヤを選択
            most_voted_players: List[Player] = await self.get_most_voted_players(p_list)
            for mvp in most_voted_players:
                await ctx.send(f"{mvp.name}({mvp.after_game_role.name})が吊られました")
                await asyncio.sleep(1)

            # 一番投票数が多かったプレイヤたちに人狼陣営がいれば、村人陣営の勝利
            if await self.check_black_side_in_players(most_voted_players):
                await ctx.send("**人狼陣営を吊ったため、**")
                await asyncio.sleep(1)
                await ctx.send("**__村人陣営の勝利です！__**")
            else:
                await ctx.send("**村人陣営を吊ったため、**")
                await asyncio.sleep(1)
                await ctx.send("**__人狼陣営の勝利です！__**")

        await asyncio.sleep(1)
        await ctx.send("``` ```")

        # デバッグ用
        for p in self.player_list:
            # 怪盗に役職交換されたかどうかで文言変更
            if p.game_role.name != p.after_game_role.name:
                role_name = f"{p.game_role.name} -> {p.after_game_role.name}"
            else:
                role_name = p.after_game_role.name
            await ctx.send(f"{p.name}({role_name})への投票数は{p.vote_count}でした")
        await ctx.send(f"墓地に置いてあったカードは{self.grave_role_list}でした")
        await ctx.send("``` ```")

    async def set_game_role(self, ctx: Context) -> List:
        # 役職配布
        n: int = len(self.player_list)

        before_role_class_list = simple[n]
        role_class_list = random.sample(before_role_class_list, n + 2)
        role_list = []
        for role in role_class_list:
            role_list.append(role(self.player_list))

        # 鍵チャンネルへの権限を設定
        await self.set_channel_role(ctx)

        # 各参加者にゲーム役職を追加
        for i, player in enumerate(self.player_list):
            name: str = player.name
            role = role_list[i]

            # 送信先チャンネル取得
            channel_name: str = "join0" + str(i)
            for c in ctx.guild.channels:
                if c.name == channel_name:
                    channel = c
            # テキストセパレータ
            await channel.send("``` ```")
            await channel.send(f"{channel_name}に送信。{name}の役職は{role.name}です")

            # 各Playerのプロパティに情報設定
            player.channel = channel
            player.game_role = role
            # 怪盗に交換された後のゲームロール
            player.after_game_role = role

        # 墓地送りになった役職を取得
        self.grave_role_list.append(role_class_list[-1].name)
        self.grave_role_list.append(role_class_list[-2].name)

        # シャッフルの役職名一覧を返却
        role_name_list = [x.name for x in before_role_class_list]
        return role_name_list

    async def role_action_exec(self, ctx: Context) -> None:
        role_action_list = []
        for player in self.player_list:
            if player.game_role.name == "占い師":
                logger.debug(f"{player.game_role.name=}")
                # 占い師アクション用：墓場にあるカードを設定する
                player.game_role.grave_role_list.append(self.grave_role_list)

            # wait_for()含む処理を並列に動かすため、各役職のアクションメソッドをリストに入れる
            role_action_list.append(
                asyncio.create_task(
                    player.game_role.action(ctx, player, player.channel)
                )
            )

        # リアクションチェック用
        role_action_list.append(asyncio.create_task((self.check_react(ctx))))

        # wait_for()を含むrole_action()を並列実行
        for role_action in role_action_list:
            num = await role_action
            self.react_num += num

    async def vote_exec(self, ctx: Context) -> None:
        self.react_num = 0
        role_action_list = []
        for player in self.player_list:
            # wait_for()含む処理を並列に動かすため、各役職のアクションメソッドをリストに入れる
            role_action_list.append(
                asyncio.create_task(player.game_role.vote(ctx, player, player.channel))
            )

        # リアクションチェック用
        role_action_list.append(asyncio.create_task((self.check_react(ctx))))

        # wait_for()を含むrole_action()を並列実行
        for role_action in role_action_list:
            num = await role_action
            self.react_num += num

    async def check_react(self, ctx: Context) -> int:
        # 経過時間
        elapsed_time = 0
        # 1分が経過してリアクション数がプレイヤ数より下回っている場合催促する
        while self.react_num < len(self.player_list):
            elapsed_time = elapsed_time + 1
            await asyncio.sleep(1)

            if elapsed_time % 60 == 0:
                await ctx.send("**まだリアクション絵文字を押してない人がいます**")

        await ctx.send("**全員がリアクション絵文字を押したのを確認しました**")

        # self.check_numの加算でエラーにしなようにするため
        return 0

    async def set_channel_role(self, ctx: Context) -> None:
        player_list: List[Player] = self.player_list
        n: int = len(player_list)
        if 0 == n:
            await ctx.send("参加者は0人です")
            return
        for i, player in enumerate(player_list):
            d_role_name: str = "join0" + str(i)
            d_role: Role = utils.get(ctx.guild.roles, name=d_role_name)

            member = utils.get(ctx.guild.members, id=player.id)
            await member.add_roles(d_role)
            s: str = f"{player.name}さんは鍵チャンネル{d_role_name}にアクセス出来るようになりました"
            await ctx.send(s)

    @staticmethod
    async def is_vote_count_same_for_all(p_list: List[Player]) -> bool:
        """平和村かどうか"""
        vote_count_list: List[int] = [x.vote_count for x in p_list]

        # 重複を排除し、全て同じ
        return len(list(set(vote_count_list))) == 1

    @staticmethod
    async def check_black_side_in_players(player_list: List[Player]) -> bool:
        """プレイヤ内に人狼陣営がいるかどうか"""

        game_side_list = [x.after_game_role.side for x in player_list]
        return SideConst.BLACK in game_side_list

    @staticmethod
    async def get_most_voted_players(player_list: List[Player]) -> List[Player]:
        """一番投票されたプレイヤを返す"""
        # 投票された数とゲーム終了後の役職を取得
        voted_list = [x.vote_count for x in player_list]
        logger.debug(f"{voted_list=}")

        sorted_voted_list = []
        # 並び替えするために、取得した二つのリストを二次元配列にする
        for voted, player in zip(voted_list, player_list):
            sorted_voted_list.append((voted, player))

        logger.debug(f"{sorted_voted_list=}")
        list.sort(sorted_voted_list, key=lambda x: x[0], reverse=True)
        logger.debug(f"{sorted_voted_list=}")

        # 最多投票数
        most_voted_num: int = sorted_voted_list[0][0]
        logger.debug(f"{most_voted_num=}")

        # 最多投票数以外を除外
        voted_list = [x[1] for x in sorted_voted_list if x[0] == most_voted_num]
        logger.debug(f"{voted_list=}")

        return voted_list
