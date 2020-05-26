from discord.channel import TextChannel

from cogs.utils.gamerole import GameRole
from setup_logger import setup_logger

logger = setup_logger(__name__)


class Player:
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
        self.__game_role: GameRole = None
        # 怪盗役職交換用
        self.__after_game_role: GameRole = None

    @property
    def game_role(self) -> GameRole:
        return self.__game_role

    @game_role.setter
    def game_role(self, role: GameRole) -> None:
        self.__game_role = role

    @property
    def after_game_role(self) -> GameRole:
        return self.__after_game_role

    @after_game_role.setter
    def after_game_role(self, role: GameRole) -> None:
        self.__after_game_role = role
