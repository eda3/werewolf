from enum import Enum

from setup_logger import setup_logger

logger = setup_logger(__name__)


class GameStatus(Enum):
    logger.debug("Constのinit")
    NOTHING = "Nothing"
    PLAYING = "Playing"
    WAITING = "Waiting"
