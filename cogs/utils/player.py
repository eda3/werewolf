from discord import Member
from discord.channel import TextChannel

from cogs.utils.gamerole import GameRole
from setup_logger import setup_logger

logger = setup_logger(__name__)


class Player:
    """人狼ゲーム参加者

    Attributes:
        id: DiscordユーザID
    """

    _game_role: GameRole
    # 怪盗役職交換用
    _after_game_role: GameRole

    def __init__(self, member: Member) -> None:
        logger.debug("Playerクラス init")
        self.d_member: Member = member
        self.id: int = member.id
        self.name: str = member.display_name
        self.channel: TextChannel
        self.vote_count: int = 0

    @property
    def game_role(self) -> GameRole:
        return self._game_role

    @game_role.setter
    def game_role(self, role: GameRole) -> None:
        self._game_role = role

    @property
    def after_game_role(self) -> GameRole:
        return self._after_game_role

    @after_game_role.setter
    def after_game_role(self, role: GameRole) -> None:
        self._after_game_role = role
