from enum import Enum

from setup_logger import setup_logger

logger = setup_logger(__name__)


class GameStatusConst(Enum):
    logger.debug("Constのinit")
    NOTHING = "nothing"
    PLAYING = "playing"
    WAITING = "waiting"


join_channel_const = [
    707507341624475648,
    707507752821456906,
    711398876665348158,
    711398920881963068,
    711398963743293470,
    711398994957303840,
    711399027341656076,
    711399090281512970,
    711399128114135071,
    711399177304801290,
]

emoji_list = [
    "0⃣",
    "1⃣",
    "2⃣",
    "3⃣",
    "4⃣",
    "5⃣",
    "6⃣",
    "7⃣",
    "8⃣",
    "9⃣",
    "🔟",
]
