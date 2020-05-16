from enum import Enum

from setup_logger import setup_logger

logger = setup_logger(__name__)


class GameStatusConst(Enum):
    logger.debug("Constのinit")
    NOTHING = "nothing"
    PLAYING = "playing"
    WAITING = "waiting"
