from setup_logger import setup_logger
from cogs.utils.const import GameStatusConst

logger = setup_logger(__name__)


class Game:
    def __init__(self) -> None:
        logger.debug("Gameクラス init")
        self.status = GameStatusConst.NOTHING.value
