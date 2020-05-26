from cogs.utils.const import GameStatusConst

# from cogs.utils import player
from cogs.utils.player_list import PlayerList
from setup_logger import setup_logger

logger = setup_logger(__name__)


class Game:
    def __init__(self) -> None:
        logger.debug("Gameクラス init")
        self.status = GameStatusConst.NOTHING.value
        self.player_list: PlayerList = PlayerList()
