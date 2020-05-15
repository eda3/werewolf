from datetime import datetime as dt
from pathlib import Path

from logging import (
    getLogger,
    Logger,
    FileHandler,
    StreamHandler,
    DEBUG,
    INFO,
    Formatter,
)


def setup_logger(name: str = "", logfile: str = "LOGFILENAME.txt") -> Logger:
    # ログファイル名は年月日時分秒をつける
    dt_now: dt = dt.now()
    dt_str: str = dt_now.strftime("%Y%m%d_%H%M%S")
    log_name: str = f"log_{dt_str}.txt"

    # ログファイルの格納先
    log_name_path: Path = Path(log_name)
    log_dir_path: Path = Path("log")
    log_file_path: Path = Path(log_dir_path / log_name_path)
    logger: Logger = getLogger(name)
    logger.setLevel(DEBUG)

    # ログファイルにはINFOレベルまで表示
    fh: FileHandler = FileHandler(log_file_path)
    fh.setLevel(INFO)
    fh_formatter = Formatter(
        "%(asctime)s - %(levelname)8s - %(filename)8s - "
        "%(name)8s - %(funcName)8s - %(message)s"
    )
    fh.setFormatter(fh_formatter)

    # コンソールにはDEBUGレベルまで表示
    sh: StreamHandler = StreamHandler()
    sh.setLevel(DEBUG)
    sh_formatter = Formatter(
        "%(asctime)s - %(funcName)s() - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    sh.setFormatter(sh_formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger
