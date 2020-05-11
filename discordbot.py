import os

from discord.ext.commands import Bot, Context

# 接頭辞を「;」に設定
bot: Bot = Bot(command_prefix=";")


def main() -> None:
    token = os.environ["DISCORD_BOT_TOKEN"]
    bot.run(token)


# 「;ping」と入力したら「pong」と返ってくる
@bot.command()
async def ping(ctx: Context) -> None:
    await ctx.send("pong")


if __name__ == "__main__":
    main()
