from typing import List

from discord import Member, Message, Reaction
from discord.channel import TextChannel

from cogs.utils.const import SideConst, emoji_list
from cogs.utils.player import Player
from cogs.utils.werewolf_bot import WerewolfBot
from setup_logger import setup_logger

logger = setup_logger(__name__)


class Villager:
    """村人"""

    name = "村人"

    def __init__(self, bot: WerewolfBot) -> None:
        self.bot: WerewolfBot = bot
        self.side = SideConst.WHITE

    async def action(self, player: Player, channel: TextChannel) -> int:
        await channel.send(
            "あなたは**__村人__**です。特殊な能力はありません。"
            "村の中に潜む人狼を吊りあげ、勝利に導きましょう。"
            "メッセージを確認したら、 :zero: の絵文字リアクションをクリックしてください"
        )
        m_id: int = channel.last_message_id
        last_message: Message = await channel.fetch_message(m_id)
        await last_message.add_reaction(emoji_list[0])

        def my_check(reaction: Reaction, user: Member) -> bool:
            return user == player.d_member and str(reaction.emoji) == emoji_list[0]

        logger.debug(f"{dir(self.bot)=}")
        await self.bot.wait_for("reaction_add", check=my_check)
        await channel.send(f"{player.name}が :zero: を押したのを確認しました")
        return 1


class Werewolf:
    """人狼"""

    def __init__(self, bot: WerewolfBot) -> None:
        self.bot: WerewolfBot = bot
        self.name = "人狼"
        self.side = SideConst.BLACK

    async def action(self, player: Player, channel: TextChannel) -> int:

        first_night_message = (
            "あなたは**__人狼__**(人狼サイド)です。勝利条件は村人サイド（村人、占い師、怪盗）を吊ることです。"
            "メッセージを確認したら、 :zero: の絵文字リアクションをクリックしてください。"
        )
        await channel.send(first_night_message)

        # リストから人狼一覧を抽出
        player_list: List[Player] = self.bot.game.player_list
        werewolf_list: List[str] = []
        for p in player_list:
            if p.game_role.name == "人狼":
                werewolf_list.append(p.name)

        text = f"今回のゲームの人狼は{werewolf_list}です"
        await channel.send(text)

        m_id: int = channel.last_message_id
        last_message: Message = await channel.fetch_message(m_id)
        await last_message.add_reaction(emoji_list[0])

        def my_check(reaction: Reaction, user: Member) -> bool:
            return user == player.d_member and str(reaction.emoji) == emoji_list[0]

        logger.debug(f"{dir(self.bot)=}")
        await self.bot.wait_for("reaction_add", check=my_check)
        await channel.send(f"{player.name}が :zero: を押したのを確認しました")
        return 1


class FortuneTeller:
    """占い師"""

    def __init__(self, bot: WerewolfBot) -> None:
        self.bot: WerewolfBot = bot
        self.name = "占い師"
        self.side = SideConst.WHITE

    async def action(self, player: Player, channel: TextChannel) -> int:
        await channel.send(
            "あなたは**__占い師__**(村人サイド)です。特定の人を占い、村人サイドか人狼サイドか占うことができます"
            "村の中に潜む人狼を吊りあげ、勝利に導きましょう。占う人物を選択してください。"
        )

        # 占い対象を選択
        p_list = [x for x in self.bot.game.player_list if x is not player]
        text = ""
        choice_emoji = []
        for emoji, p in zip(emoji_list, p_list):
            choice_emoji.append(emoji)
            text += f"{emoji} {p.name}"
        await channel.send(text)

        m_id: int = channel.last_message_id
        last_message: Message = await channel.fetch_message(m_id)
        for emoji in choice_emoji:
            await last_message.add_reaction(emoji)

        def my_check(reaction: Reaction, user: Member) -> bool:
            return user == player.d_member and str(reaction.emoji) in choice_emoji

        react_emoji, react_user = await self.bot.wait_for(
            "reaction_add", check=my_check
        )
        await channel.send(f"{react_user.name}が {react_emoji.emoji} を押したのを確認しました")

        # リアクション絵文字から、プレイヤを逆引き
        p_name: str = ""
        p_side: SideConst = SideConst.WHITE
        for i, emoji in enumerate(choice_emoji):
            if emoji == react_emoji.emoji:
                p_name = p_list[i].name
                p_side = p_list[i].game_role.side
        await channel.send(f"占い結果：{p_name}は{p_side.value}です。")

        return 1


class Thief:
    """怪盗"""

    def __init__(self, bot: WerewolfBot) -> None:
        self.bot: WerewolfBot = bot
        self.name = "怪盗"
        self.side = SideConst.WHITE

    async def action(self, player: Player, channel: TextChannel) -> int:
        await channel.send(
            "あなたは**__怪盗__**(村人サイド)です。特定の人の役職と自分の役職をすりかえることが出来ます"
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


"""
役職編成の辞書
村: 村人
狼: 人狼
占: 占い師
"""
simple = {
    # 3: 村村占狼盗
    3: [Villager, Villager, FortuneTeller, Werewolf, Thief],
    # 4: 村村占狼狼盗
    4: [Villager, Villager, FortuneTeller, Werewolf, Werewolf, Thief],
    # 5: 村村村占狼狼盗
    5: [Villager, Villager, Villager, FortuneTeller, Werewolf, Werewolf, Thief],
}
