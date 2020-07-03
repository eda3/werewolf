from __future__ import annotations
from typing import List
from discord import Emoji, Member, Message, Reaction, utils
from discord.channel import TextChannel
from discord.ext.commands import Context

from games.gamerole import GameRole
from games.const import emoji_list


class Player:
    """人狼ゲーム参加者

    Attributes:
        id: DiscordユーザID
    """

    def __init__(self, discord_id: int, name: str):
        self.discord_id: int = discord_id
        self.name: str = name
        self.channel: TextChannel
        self.vote_count: int = 0
        self.vote_target: str = ""
        self.game_role: GameRole  # 怪盗交換前
        self.after_game_role: GameRole  # 怪盗交換後

    async def vote(
        self, ctx: Context, player_list: List[Player], channel: TextChannel
    ) -> int:
        await channel.send("``` ```")
        await channel.send("人狼だと思う人を一人選択してください")

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

        def my_check(reaction: Reaction, user: Member) -> bool:
            member: Member = utils.get(ctx.bot.get_all_members(), id=self.discord_id)
            return user == member and str(reaction.emoji) in choice_emoji

        react_emoji, react_user = await ctx.bot.wait_for("reaction_add", check=my_check)
        await channel.send(f"{react_user.name}が {react_emoji.emoji} を押したのを確認しました")

        # リアクション絵文字から、プレイヤを逆引き
        p_idx: int = 0
        for i, emoji in enumerate(choice_emoji):
            if emoji == react_emoji.emoji:
                p_idx = i

        player_list[p_idx].vote_count += 1
        choice_player: Player = player_list[p_idx]

        self.vote_target = choice_player.name
        await channel.send(f"あなたは{self.vote_target}に投票しました")

        return 1
