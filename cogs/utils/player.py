from setup_logger import setup_logger

logger = setup_logger(__name__)


class Player:
    """人狼ゲーム参加者

    Attributes:
        id: DiscordユーザID
    """

    def __init__(self, discord_id: int) -> None:
        logger.debug("Playerクラス init")
        self.id: int = discord_id
