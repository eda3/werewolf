from discord.ext.commands import Bot, Cog, command, context

from cogs.utils.player import Player


class GameStatusCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=["sgs"])
    async def show_game_status(self, ctx: context) -> None:
        await ctx.send("show_game_statusコマンドが実行されました")
        # TODO: ゲームステータスを表示する


def setup(bot: Bot) -> None:
    bot.add_cog(GameStatusCog(bot))
