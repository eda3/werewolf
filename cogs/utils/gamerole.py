from abc import ABCMeta, abstractmethod

from discord.channel import TextChannel

from cogs.utils.const import SideConst
from cogs.utils.werewolf_bot import WerewolfBot


class GameRole(metaclass=ABCMeta):
    """各役職の抽象クラス"""

    def __init__(self, bot: WerewolfBot) -> None:
        self.bot: WerewolfBot
        self.name = ""
        self.side = SideConst.WHITE

