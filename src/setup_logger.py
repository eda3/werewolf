from logging import DEBUG, Formatter, Logger, StreamHandler, getLogger


def setup_logger(name: str = "") -> Logger:
    logger: Logger = getLogger(name)
    logger.setLevel(DEBUG)

    # コンソールにはDEBUGレベルまで表示
    sh: StreamHandler = StreamHandler()
    sh.setLevel(DEBUG)
    sh_formatter = Formatter(
        "%(asctime)s - %(filename)s - %(funcName)s() - " "%(levelname)s - %(message)s",
        "%Y%m%d %H%M%S",
    )
    sh.setFormatter(sh_formatter)

    logger.addHandler(sh)
    return logger
