import os

from discord.ext.commands import Bot


bot: Bot = Bot(command_prefix=";")
print(f"{type(bot)=}")

def main():
    token = os.environ["DISCORD_BOT_TOKEN"]
    print(f"{type(token)=}")
    print(token)
    bot.run(token)


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


if __name__ == "__main__":
    main()
