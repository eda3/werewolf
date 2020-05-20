from discord import Member
from discord.channel import TextChannel
from setup_logger import setup_logger

logger = setup_logger(__name__)


class Player:
    """人狼ゲーム参加者

    Attributes:
        id: DiscordユーザID
    """

    def __init__(self, member: Member) -> None:
        logger.debug("Playerクラス init")
        self.d_member: Member = member
        self.id: int = member.id
        self.name: str = member.display_name
        self.channel: TextChannel
        self._game_role = None

    @property
    def game_role(self):
        return self._game_role

    @game_role.setter
    def game_role(self, role) -> None:
        self._game_role = role

