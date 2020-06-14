from enum import Enum

from setup_logger import setup_logger

logger = setup_logger(__name__)


class GameStatusConst(Enum):
    logger.debug("Constのinit")
    NOTHING = "nothing"
    PLAYING = "playing"
    WAITING = "waiting"


# アルファベット絵文字のA～Z
emoji_list = [
    "\N{regional indicator symbol letter a}",
    "\N{regional indicator symbol letter b}",
    "\N{regional indicator symbol letter c}",
    "\N{regional indicator symbol letter d}",
    "\N{regional indicator symbol letter e}",
    "\N{regional indicator symbol letter f}",
    "\N{regional indicator symbol letter g}",
    "\N{regional indicator symbol letter h}",
    "\N{regional indicator symbol letter i}",
    "\N{regional indicator symbol letter j}",
    "\N{regional indicator symbol letter k}",
    "\N{regional indicator symbol letter l}",
    "\N{regional indicator symbol letter m}",
    "\N{regional indicator symbol letter n}",
    "\N{regional indicator symbol letter o}",
    "\N{regional indicator symbol letter p}",
    "\N{regional indicator symbol letter q}",
    "\N{regional indicator symbol letter r}",
    "\N{regional indicator symbol letter s}",
    "\N{regional indicator symbol letter t}",
    "\N{regional indicator symbol letter u}",
    "\N{regional indicator symbol letter v}",
    "\N{regional indicator symbol letter w}",
    "\N{regional indicator symbol letter x}",
    "\N{regional indicator symbol letter y}",
    "\N{regional indicator symbol letter z}",
]


class SideConst(Enum):
    WHITE = "村人陣営(白)"
    BLACK = "人狼陣営(黒)"


DISCUSSION_TIME = 300
