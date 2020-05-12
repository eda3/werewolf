import os

from discord.ext.commands import Bot, Context, command


def main() -> None:
    # 接頭辞を「;」に設定
    bot: Bot = Bot(command_prefix=";")

    # 環境変数DISCORD_BOT_TOKENからBOTのトークンを取得
    token = os.environ["DISCORD_BOT_TOKEN"]

    # コマンド「;ping」を追加
    # コマンドの内容は ping()を参照
    bot.add_command(ping)

    # bot実行
    bot.run(token)


@command()
async def ping(ctx: Context) -> None:
    """「;ping」と入力したら「pong」と返ってくる

    :param ctx:
    :return: None
    """
    await ctx.send("pong")


if __name__ == "__main__":
    main()
