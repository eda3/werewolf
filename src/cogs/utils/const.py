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

"""
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
"""

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
