from sqlalchemy import create_engine
from gpm import config, logging

cfg = config.Config()
cfg.read()


def do():
    errcode = 0
    return errcode


if __name__ == "__main__":
    exit(do())
