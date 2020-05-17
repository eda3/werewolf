from enum import Enum

from setup_logger import setup_logger

logger = setup_logger(__name__)


class GameStatusConst(Enum):
    logger.debug("Constのinit")
    NOTHING = "nothing"
    PLAYING = "playing"
    WAITING = "waiting"


join_channel_const = {
    0: 707507341624475648,
    1: 707507752821456906,
    2: 711398876665348158,
    3: 711398920881963068,
    4: 711398963743293470,
    5: 711398994957303840,
    6: 711399027341656076,
    7: 711399090281512970,
    8: 711399128114135071,
    9: 711399177304801290,
}

"""
join_channel_const = {
    JOIN0: 707507341624475648,
    JOIN1: 707507341624475648,
    JOIN2: 707507752821456906,
    JOIN3: 711398876665348158,
    JOIN4: 711398963743293470,
    JOIN5: 711398994957303840,
    JOIN6: 711399128114135071,
    JOIN7: 711399090281512970,
    JOIN8: 711399128114135071,
    JOIN9: 711399177304801290,
}

"""
