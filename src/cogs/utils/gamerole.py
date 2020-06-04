from typing import List

from discord.ext.commands import Context
from discord import Emoji, Member, Message, Reaction, utils
from discord.channel import TextChannel

from cogs.utils.const import SideConst, emoji_list


class GameRole:
    """各役職のスーパークラス"""

    def __init__(self, player_list) -> None:
        self.player_list = player_list
        self.name = ""
        self.side = SideConst.WHITE

    async def vote(self, ctx: Context, player, channel: TextChannel) -> int:
        await channel.send("``` ```")
        await channel.send("人狼だと思う人を一人選択してください")

        choice_player = await self.select_player(ctx, player, channel)

        player.vote_target = choice_player.name
        await channel.send(f"あなたは{player.vote_target}に投票しました")

        return 1

    async def select_player(self, ctx: Context, player, channel: TextChannel):
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
