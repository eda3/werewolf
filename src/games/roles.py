from typing import List

from discord import Emoji, Member, Message, Reaction
from discord.channel import TextChannel
from discord.ext.commands import Bot

from games.const import SideConst, emoji_list
from games.gamerole import GameRole
from games.player import Player


class Villager(GameRole):
    """村人"""

    name: str = ":man:村人"
    side: str = SideConst.WHITE

    def __init__(self) -> None:
        pass

    @staticmethod
    async def action(
        bot: Bot, player_list: List[Player], player: Player, channel: TextChannel
    ) -> int:

        await channel.send(
            "あなたは**__村人__**です。特殊な能力はありません。"
            "村の中に潜む人狼を吊りあげ、勝利に導きましょう。"
            f"メッセージを確認したら、 {emoji_list[0]} の絵文字リアクションをクリックしてください"
        )
        m_id: int = channel.last_message_id
        last_message: Message = await channel.fetch_message(m_id)
        await last_message.add_reaction(emoji_list[0])

        def my_check(reaction: Reaction, user: Member) -> bool:
            check1: bool = user.id == player.discord_id
            check2: bool = reaction.emoji == emoji_list[0]
            return check1 and check2

        await bot.wait_for("reaction_add", check=my_check)
        await channel.send(f"{player.name}が {emoji_list[0]} を押したのを確認しました")
        return 1


class Werewolf:
    """人狼"""

    name: str = ":wolf:人狼"
    side: str = SideConst.BLACK

    def __init__(self) -> None:
        pass

    @staticmethod
    async def action(
        bot: Bot, player_list: List[Player], player: Player, channel: TextChannel
    ) -> int:
        await channel.send("あなたは:wolf:**__人狼__**(人狼陣営)です。\n")

        werewolf_list: List[str] = []
        for p in player_list:
            if p.game_role.name == Werewolf.name:
                werewolf_list.append(p.name)

        text: str = f"今回のゲームの人狼は以下の__**{len(werewolf_list)}人**__です。\n"

        for werewolf in werewolf_list:
            text += ":wolf:" + werewolf + "\n"

        await channel.send(text)
        first_night_message: str = (
            "勝利条件は村人陣営（村人、占い師、怪盗）を吊ることです。"
            f"メッセージを確認したら、 {emoji_list[0]} の絵文字リアクションをクリックしてください。\n"
        )
        await channel.send(first_night_message)

        m_id: int = channel.last_message_id
        last_message: Message = await channel.fetch_message(m_id)
        await last_message.add_reaction(emoji_list[0])

        def my_check(reaction: Reaction, user: Member) -> bool:
            check1: bool = user.id == player.discord_id
            check2: bool = reaction.emoji == emoji_list[0]
            return check1 and check2

        await bot.wait_for("reaction_add", check=my_check)
        await channel.send(f"{player.name}が {emoji_list[0]} を押したのを確認しました")
        return 1


class FortuneTeller:
    """占い師"""

    name: str = ":mage:占い師"
    side: str = SideConst.WHITE

    def __init__(self) -> None:
        # 墓場にあるカード
        self.grave_role_list: List[GameRole] = []

    async def action(
        self, bot: Bot, player_list: List[Player], player: Player, channel: TextChannel
    ) -> int:
        await channel.send(
            "あなたは**__占い師__**(村人陣営)です。特定の人を占い、村人陣営か人狼陣営か占うことができます"
            "村の中に潜む人狼を吊りあげ、勝利に導きましょう。占う人物を選択してください。"
        )

        # 占い対象を選択
        choice: Player = await self.fortune_telling(bot, player_list, player, channel)

        # プレイヤーを選択した場合
        if isinstance(choice, Player):
            name: str = choice.name
            side: str = choice.game_role.side.value
            await channel.send(f"占い結果：{name}は{side}です。")
        else:
            await channel.send(f"占い結果：墓場に置かれた役職は{choice[0]}です")
        return 1

    async def fortune_telling(
        self, bot: Bot, player_list: List[Player], player: Player, channel: TextChannel
    ) -> Player:

        # 対象を選択
        another_player_list: List[Player] = [x for x in player_list if x is not player]

        text: str = ""
        choice_emoji: List[Emoji] = []
        for i in range(len(another_player_list)):
            choice_emoji.append(emoji_list[i])
            text += f"{emoji_list[i]} {another_player_list[i].name}"

        # 一番最後に墓場用の絵文字を追加
        i = i + 1
        choice_emoji.append(emoji_list[i])
        text += f"{emoji_list[i]} 墓場のカード2枚"

        await channel.send(text)

        m_id: int = channel.last_message_id
        last_message: Message = await channel.fetch_message(m_id)
        for emoji in choice_emoji:
            await last_message.add_reaction(emoji)

        def my_check(user: Member) -> bool:
            return user.id == player.discord_id

        react_emoji, react_user = await bot.wait_for("reaction_add", check=my_check)
        await channel.send(f"{react_user.name}が {react_emoji.emoji} を押したのを確認しました")

        # リアクション絵文字から、プレイヤを逆引き
        p_idx: int = 0
        for i, emoji in enumerate(choice_emoji):
            if emoji == react_emoji.emoji:
                p_idx = i

        if len(player_list) == p_idx:
            return self.grave_role_list
        else:
            return player_list[p_idx]


class Thief:
    """怪盗"""

    name: str = ":supervillain:怪盗"
    side: str = SideConst.WHITE

    def __init__(self) -> None:
        pass

    async def action(
        self, bot: Bot, player_list: List[Player], player: Player, channel: TextChannel
    ) -> int:
        await channel.send(
            "あなたは**__怪盗__**(村人陣営)です。特定の人の役職と自分の役職をすりかえることが出来ます。"
            "村の中に潜む人狼を吊りあげ、勝利に導きましょう。"
        )

        # 役職交換する自分以外のプレイヤーを選択
        choice_player: Player = await self.select_player(
            bot, player_list, player, channel
        )

        # 選択プレイヤーと自分の役職を交換
        temp_role: GameRole = player.game_role
        player.after_game_role = choice_player.game_role
        choice_player.after_game_role = temp_role

        # メッセージ送信用にプレイヤー名と役職名を取得
        choice_player_name: str = choice_player.game_role.name
        choice_player_game_role: str = choice_player.game_role.name
        choice_player_after_game_role: str = choice_player.after_game_role.name
        player_game_role_name: str = player.after_game_role.name
        await channel.send(
            f"あなたは{choice_player_name}と役職交換しました。\n"
            f"{choice_player_name}の役職は{choice_player_game_role}でした。\n"
            f"{choice_player_name}の現在の役職は{choice_player_after_game_role}です。\n"
            f"あなたの現在の役職は{player_game_role_name}です。"
        )
        return 1

    @staticmethod
    async def select_player(
        bot: Bot, player_list: List[Player], player: Player, channel: TextChannel
    ) -> Player:

        text: str = ""
        choice_emoji: List[Emoji] = []
        for emoji, player in zip(emoji_list, player_list):
            choice_emoji.append(emoji)
            text += f"{emoji} {player.name}"
        await channel.send(text)

        m_id: int = channel.last_message_id
        last_message: Message = await channel.fetch_message(m_id)
        for emoji in choice_emoji:
            await last_message.add_reaction(emoji)

        def my_check(user: Member) -> bool:
            return user.id == player.discord_id

        react_emoji, react_user = await bot.wait_for("reaction_add", check=my_check)
        await channel.send(f"{react_user.name}が {react_emoji.emoji} を押したのを確認しました")

        # リアクション絵文字から、プレイヤを逆引き
        p_idx: int = 0
        for i, emoji in enumerate(choice_emoji):
            if emoji == react_emoji.emoji:
                p_idx = i

        return player_list[p_idx]


class HangedMan:
    """吊人"""

    name: str = ":upside_down:吊人"
    side: str = SideConst.WHITE

    def __init__(self) -> None:
        pass

    async def action(
        self, bot: Bot, player_list: List[Player], player: Player, channel: TextChannel
    ) -> int:
        await channel.send(
            f"あなた({player.name})は**__吊人__**(村人陣営)です。勝利条件は**自分が吊られること**です。"
            f"自分を人狼だと思わせ、自分が吊られることになったらあなた({player.name})の一人勝ちです。"
        )
        await channel.send(
            f"ただし、平和村＝人狼陣営がいない場合、あなた({player.name})は吊られてはいけません。普通の村人として行動しましょう"
            f"メッセージを確認したら、 {emoji_list[0]} の絵文字リアクションをクリックしてください"
        )
        m_id: int = channel.last_message_id
        last_message: Message = await channel.fetch_message(m_id)
        await last_message.add_reaction(emoji_list[0])

        def my_check(reaction: Reaction, user: Member) -> bool:
            check1: bool = user.id == player.discord_id
            check2: bool = reaction.emoji == emoji_list[0]
            return check1 and check2

        await bot.wait_for("reaction_add", check=my_check)
        await channel.send(f"{player.name}が {emoji_list[0]} を押したのを確認しました")
        return 1


simple = {
    # 2: 村占盗狼
    2: [Villager, FortuneTeller, Thief, Werewolf],
    # 3: 村村占狼盗
    3: [Villager, Villager, FortuneTeller, Thief, Werewolf],
    # 3: [Villager, Villager, Villager, Werewolf, Werewolf],
    # 4: 村村占狼狼盗
    # 4: [Villager, Villager, FortuneTeller, Thief, Werewolf, Werewolf],
    4: [HangedMan, Villager, FortuneTeller, Thief, Werewolf, Werewolf],
    # 5: 村村占狼狼盗吊
    5: [Villager, Villager, FortuneTeller, Thief, Werewolf, Werewolf, HangedMan],
    # 6:村村村占狼狼盗吊
    6: [
        Villager,
        Villager,
        Villager,
        FortuneTeller,
        Thief,
        Werewolf,
        Werewolf,
        HangedMan,
    ],
}
