#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest
from stock import Descriptor, SizedString, UnsignedInteger, UnsignedFloat


def validate_attributes(**kwargs):
    def decorate_cls(cls):
        for attr, descriptor in kwargs.items():
            if isinstance(descriptor, Descriptor):
                descriptor.__set_name__(cls, attr)
            setattr(cls, attr, descriptor)
        return cls

    return decorate_cls


@validate_attributes(
    name=SizedString(max_len=8),
    shares=UnsignedInteger,
    price=UnsignedFloat,
)
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


# if __name__ == "__main__":
#     stock = Stock("ACME", 50, 91.1)


@pytest.fixture
def stock():
    return Stock("ACME", 50, 91.1)


def test_stock(stock):
    assert stock.name == "ACME"
    assert stock.shares == 50
    assert stock.price == 91.1
