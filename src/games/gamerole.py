from abc import ABC


class GameRole(ABC):
    """各役職の抽象クラス"""

    name: str
    side: str
