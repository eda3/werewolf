from typing import TypeVar, Generic
from discord.channel import TextChannel

from setup_logger import setup_logger

logger = setup_logger(__name__)


T = TypeVar("T")


class Player(Generic[T]):
    """人狼ゲーム参加者

    Attributes:
        id: DiscordユーザID
    """

    def __init__(self, d_id: int, name: str):
        logger.debug("Playerクラス init")
        self.id: int = d_id
        self.name: str = name
        self.channel: TextChannel
        self.vote_count: int = 0
        self.__game_role: T = ""
        # 怪盗役職交換用
        self.__after_game_role: T = ""
        self.vote_target = ""

    @property
    def game_role(self) -> T:
        return self.__game_role

    @game_role.setter
    def game_role(self, role: T) -> None:
        self.__game_role = role

    @property
    def after_game_role(self) -> T:
        return self.__after_game_role

    @after_game_role.setter
    def after_game_role(self, role: T) -> None:
        self.__after_game_role = role
