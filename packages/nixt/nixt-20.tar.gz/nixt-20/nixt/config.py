# This file is placed in the Public Domain.
# pylint: disable=C,I,R,W0201


"configuration"


import os


from .default import Default
from .persist import Persist


class Config(Default):

    "Config"


def config(path=None):
    cfg         = Config()
    cfg.name    = config.__module__.rsplit(".", maxsplit=2)[-2]
    cfg.wdr     = path or os.path.expanduser(f"~/.{cfg.name}")
    cfg.pidfile = os.path.join(cfg.wdr, f"{cfg.name}.pid")
    Persist.workdir = cfg.wdr
    return cfg


def __dir__():
    return (
        "Config",
        'config'
    )
