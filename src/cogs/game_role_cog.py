from discord.ext.commands import Bot, Cog, Context, command

from games.roles import simple


class GameRoleCog(Cog):
    @command(aliases=["sr"])
    async def show_role(self, ctx: Context, player_count: int) -> None:
        """役職一覧を表示(引数：プレイ人数)"""
        send_message: str = f"{player_count}人プレイ役職：\n"
        for role in simple[player_count]:
            send_message += str(role.name) + "\n"
        await ctx.send(send_message)


def setup(bot: Bot) -> None:
    bot.add_cog(GameRoleCog(bot))
