#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import logging
import os
import pytest

logging.basicConfig(
    filename=f".{os.path.splitext(os.path.basename(__file__))[0]}.log",
    filemode="w",
    format="%(asctime)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger(name=__name__)

logging.basicConfig()
logger = logging.getLogger(__name__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        logger.info(f"{cls = }, {args = }, {kwargs = }")
        if cls not in type(cls)._instances:
            type(cls)._instances[cls] = super().__call__(*args, **kwargs)
        return type(cls)._instances[cls]


class Spam(metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        print("Spam object has created")


if __name__ == "__main__":
    s1 = Spam()
    s2 = Spam()
    assert s1 is s2
