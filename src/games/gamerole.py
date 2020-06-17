from games.const import SideConst


class GameRole:
    """各役職のスーパークラス"""

    name: str

    def __init__(self) -> None:
        self.side: str = SideConst.WHITE
