from typing import TYPE_CHECKING, List

from discord import Emoji, Member, Message, Reaction, utils
from discord.channel import TextChannel
from discord.ext.commands import Context

from games.const import SideConst, emoji_list

from games.player import Player


class GameRole:
    """各役職のスーパークラス"""

    name: str

    def __init__(self, player_list: List[Player]) -> None:
        self.player_list: List[Player] = player_list
        self.side: str = SideConst.WHITE

    async def vote(self, ctx: Context, player: Player, channel: TextChannel) -> int:
        await channel.send("``` ```")
        await channel.send("人狼だと思う人を一人選択してください")

        choice_player: Player = await self.select_player(ctx, player, channel)

        player.vote_target = choice_player.name
        await channel.send(f"あなたは{player.vote_target}に投票しました")

        return 1

    async def select_player(
        self, ctx: Context, player: Player, channel: TextChannel
    ) -> Player:
        # 対象を選択
        p_list = self.player_list
        text: str = ""
        choice_emoji: List[Emoji] = []
        for emoji, p in zip(emoji_list, self.player_list):
            choice_emoji.append(emoji)
            text += f"{emoji} {p.name}"
        await channel.send(text)

        m_id: int = channel.last_message_id
        last_message: Message = await channel.fetch_message(m_id)
        for emoji in choice_emoji:
            await last_message.add_reaction(emoji)

        def my_check(reaction: Reaction, user: Member) -> bool:
            member = utils.get(ctx.bot.get_all_members(), id=player.id)
            return user == member and str(reaction.emoji) in choice_emoji

        react_emoji, react_user = await ctx.bot.wait_for("reaction_add", check=my_check)
        await channel.send(f"{react_user.name}が {react_emoji.emoji} を押したのを確認しました")

        # リアクション絵文字から、プレイヤを逆引き
        p_idx = 0
        for i, emoji in enumerate(choice_emoji):
            if emoji == react_emoji.emoji:
                p_idx = i

        p_list[p_idx].vote_count += 1
        return p_list[p_idx]
