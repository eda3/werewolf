from typing import List
from discord import Emoji, Member, Message, Reaction
from discord.channel import TextChannel
from discord.ext.commands import Bot

from cogs.utils.const import SideConst, emoji_list
from cogs.utils.gamerole import GameRole
from cogs.utils.player import Player
from cogs.utils.werewolf_bot import WerewolfBot
from setup_logger import setup_logger

logger = setup_logger(__name__)

"""
class GameRole(metaclass=ABCMeta):
    各役職の抽象クラス

    def __init__(self, bot: WerewolfBot) -> None:
        self.bot: WerewolfBot
        self.name = ""
        self.side = SideConst.WHITE

    @abstractmethod
    async def action(self, pl, channel: TextChannel) -> int:
        pass
"""


class Villager(GameRole):
    """村人"""

    def __init__(self, bot: WerewolfBot) -> None:
        super().__init__(bot)
        self.bot: WerewolfBot = bot
        self.name = "村人"
        self.side = SideConst.WHITE

    async def action(self, player: Player, channel: TextChannel) -> int:
        await channel.send(
            "あなたは**__村人__**です。特殊な能力はありません。"
            "村の中に潜む人狼を吊りあげ、勝利に導きましょう。"
            f"メッセージを確認したら、 {emoji_list[0]} の絵文字リアクションをクリックしてください"
        )
        m_id: int = channel.last_message_id
        last_message: Message = await channel.fetch_message(m_id)
        await last_message.add_reaction(emoji_list[0])

        def my_check(reaction: Reaction, user: Member) -> bool:
            return user == player.d_member and str(reaction.emoji) == emoji_list[0]

        await self.bot.wait_for("reaction_add", check=my_check)
        await channel.send(f"{player.name}が :zero: を押したのを確認しました")
        return 1


class Werewolf(GameRole):
    """人狼"""

    def __init__(self, bot: WerewolfBot) -> None:
        super().__init__(bot)
        self.bot: WerewolfBot = bot
        self.name = "人狼"
        self.side = SideConst.BLACK

    async def action(self, player: Player, channel: TextChannel) -> int:

        first_night_message = (
            "あなたは**__人狼__**(人狼陣営)です。勝利条件は村人陣営（村人、占い師、怪盗）を吊ることです。"
            f"メッセージを確認したら、 {emoji_list[0]} の絵文字リアクションをクリックしてください"
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

        await self.bot.wait_for("reaction_add", check=my_check)
        await channel.send(f"{player.name}が :zero: を押したのを確認しました")
        return 1


class FortuneTeller(GameRole):
    """占い師"""

    def __init__(self, bot: WerewolfBot) -> None:
        super().__init__(bot)
        self.bot: WerewolfBot = bot
        self.name = "占い師"
        self.side = SideConst.WHITE

    async def action(self, player: Player, channel: TextChannel) -> int:
        await channel.send(
            "あなたは**__占い師__**(村人陣営)です。特定の人を占い、村人陣営か人狼陣営か占うことができます"
            "村の中に潜む人狼を吊りあげ、勝利に導きましょう。占う人物を選択してください。"
        )

        # 占い対象を選択
        choice_player = await select_player(self.bot, player, channel)

        name = choice_player.name
        side = choice_player.game_role.side.value
        await channel.send(f"占い結果：{name}は{side}です。")

        return 1


class Thief(GameRole):
    """怪盗"""

    def __init__(self, bot: WerewolfBot) -> None:
        super().__init__(bot)
        self.bot: WerewolfBot = bot
        self.name = "怪盗"
        self.side = SideConst.WHITE

    async def action(self, player: Player, channel: TextChannel) -> int:
        await channel.send(
            "あなたは**__怪盗__**(村人陣営)です。特定の人の役職と自分の役職をすりかえることが出来ます。"
            "村の中に潜む人狼を吊りあげ、勝利に導きましょう。"
            f"メッセージを確認したら、 {emoji_list[0]} の絵文字リアクションをクリックしてください"
        )

        # 役職交換する自分以外のプレイヤーを選択
        choice_player = await select_player(self.bot, player, channel)

        # 選択プレイヤーと自分の役職を交換
        temp_role = player.game_role
        player.after_game_role = choice_player.game_role
        choice_player.after_game_role = temp_role

        await channel.send(
            f"あなたは{choice_player.name}と役職交換しました。"
            f"{choice_player.name}の現在役職は{choice_player.after_game_role.name}です。"
            f"あなたの現在の役職は{player.after_game_role.name}です。"
        )
        return 1


async def select_player(bot: Bot, player: Player, channel: TextChannel) -> Player:
    # 対象を選択
    p_list = [x for x in bot.game.player_list if x is not player]
    text: str = ""
    choice_emoji: List[Emoji] = []
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

    react_emoji, react_user = await bot.wait_for("reaction_add", check=my_check)
    await channel.send(f"{react_user.name}が {react_emoji.emoji} を押したのを確認しました")

    # リアクション絵文字から、プレイヤを逆引き
    p_idx = 0
    for i, emoji in enumerate(choice_emoji):
        if emoji == react_emoji.emoji:
            p_idx = i

    return p_list[p_idx]


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
    # 4: [Villager, Villager, FortuneTeller, Werewolf, Werewolf, Thief],
    4: [FortuneTeller, Werewolf, Werewolf, Thief],
    # 5: 村村村占狼狼盗
    5: [Villager, Villager, Villager, FortuneTeller, Werewolf, Werewolf, Thief],
}
