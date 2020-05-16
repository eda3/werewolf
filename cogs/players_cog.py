from discord.ext.commands import Bot, Cog, command, context

from cogs.utils.player import Player


class PlayersCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def join(self, ctx: context):
        await ctx.send("joinコマンドが実行されました")


def setup(bot):
    bot.add_cog(PlayersCog(bot))
