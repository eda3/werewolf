from typing import List

from discord import Member, Message, Reaction
from discord.channel import TextChannel

from cogs.utils.const import emoji_list
from cogs.utils.player import Player
from cogs.utils.werewolf_bot import WerewolfBot
from setup_logger import setup_logger

logger = setup_logger(__name__)


"""
役職編成の辞書
村: 村人
狼: 人狼
占: 占い師
"""

simple = {
    1: "村",
    2: "村狼",
    3: "村狼狼",
    4: "村狼占狼",
    5: "村村狼占狼",
    6: "村村村狼占狼",
    7: "村村村村狼占狼",
    8: "村村村村狼狼占村",
    9: "村村村村村狼狼占村",
    10: "村村村村狼狼占狼村村",
    11: "村村村村村狼狼占狼村村",
    12: "村村村村村村狼狼占狼村村",
    13: "村村村村村村村狼狼占狼村村",
    14: "村村村村村村村村狼狼占狼村村",
    15: "村村村村村村村村村狼狼占狼村村",
    16: "村村村村村村村狼狼狼占狼村村村村",
}


class Villager:
    """村人"""

    name = "村人"

    def __init__(self, bot: WerewolfBot) -> None:
        self.bot: Werewolf = bot

    async def action(self, player: Player, channel: TextChannel) -> int:
        await channel.send(
            "あなたは村人です。特殊な能力はありません。"
            "村の中に潜む人狼を吊りあげ、勝利に導きましょう。"
            "メッセージを確認したら、 :zero: の絵文字リアクションをクリックしてください"
        )
        m_id: int = channel.last_message_id
        last_message: Message = await channel.fetch_message(m_id)
        await last_message.add_reaction(emoji_list[0])

        def my_check(reaction: Reaction, user: Member) -> bool:
            return user == player.d_member and str(reaction.emoji) == emoji_list[0]

        await self.bot.wait_for("reaction_add", check=my_check)
        await channel.send(f"{player.name}が :zero: を押したのを確認しました")
        return 1


class Werewolf:
    """人狼"""

    def __init__(self, bot: WerewolfBot) -> None:
        self.bot: WerewolfBot = bot
        self.name = "狼"

    async def action(self, player: Player, channel: TextChannel) -> int:

        first_night_message = (
            "あなたは人狼です。勝利条件は村人サイド（村人、占い師、怪盗）を吊ることです。"
            "メッセージを確認したら、 :zero: の絵文字リアクションをクリックしてください。"
        )
        await channel.send(first_night_message)

        # リストから人狼一覧を抽出
        player_list: List[Player] = self.bot.game.player_list
        werewolf_list: List[str] = []
        for p in player_list:
            if p.game_role.name == "狼":
                werewolf_list.append(p.name)

        text = f"今回のゲームの人狼は{werewolf_list}です"
        await channel.send(text)

        m_id: int = channel.last_message_id
        last_message: Message = await channel.fetch_message(m_id)
        await last_message.add_reaction(emoji_list[0])

        def my_check(reaction: Reaction, user: Member) -> bool:
            return user == player.d_member and str(reaction.emoji) == emoji_list[0]

        await self.bot.wait_for("reaction_add", check=my_check)
        await channel.send(f"{player.name}が :zero: を押したのを確認しました")
        return 1
