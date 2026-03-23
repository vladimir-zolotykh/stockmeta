#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest
import os
import logging
from stock import Descriptor, SizedString, UnsignedInteger, UnsignedFloat, Percentage

logging.basicConfig(
    filename=f".{os.path.splitext(os.path.basename(__file__))[0]}.log",
    filemode="w",
    format="%(asctime)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger(name=__name__)


class StockMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        logger.info(f"{mcls = }, {clsname = }, {clsdict = }")
        annotations = clsdict.get("__annotations__", {})
        MISSING = object()
        fields = {}
        for attr, _type in annotations.items():
            default = clsdict[attr] if attr in clsdict else MISSING
            fields[attr] = {"type": _type, "default": default}
            if issubclass(_type, Descriptor):
                clsdict[attr] = _type() if default is MISSING else _type(**default)
        clsdict["_fields"] = fields
        return super().__new__(mcls, clsname, bases, clsdict)


class Stock(metaclass=StockMeta):
    name: SizedString = {"min_len": 0, "max_len": 12}
    shares: UnsignedInteger
    price: UnsignedFloat
    discount: Percentage

    def __init__(self, name, shares, price, discount):
        self.name = name
        self.shares = shares
        self.price = price
        self.discount = discount


@pytest.fixture
def stock():
    return Stock("ACME", 50, 91.1, 75)


def test_run_StockMeta(stock):
    assert stock.shares == 50
    assert stock.name == "ACME"
    assert stock.price == 91.1
    assert stock.discount == 75


if __name__ == "__main__":
    import sys

    pytest.main(sys.argv)
