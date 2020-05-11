import os

from discord.ext.commands import Bot, Context


bot: Bot = Bot(command_prefix=";")
print(f"{type(bot)=}")


def main() -> None:
    token = os.environ["DISCORD_BOT_TOKEN"]
    bot.run(token)


@bot.command()
async def ping(ctx: Context) -> None:
    print(f"{type(ctx)=}")
    await ctx.send("pong")


if __name__ == "__main__":
    main()
