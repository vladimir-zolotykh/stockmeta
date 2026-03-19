#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
class Descriptor:
    def __init__(self, *args, **kw):
        pass


# fmt: off
class SizedString(Descriptor): pass  # noqa: E701
class UnsignedInteger(Descriptor): pass  # noqa: E701
class UnsignedFloat(Descriptor): pass  # noqa: E701
# fmt: on


class DebugMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        for key, value in clsdict.items():
            print(f"{key}: {value}")
        return super().__new__(mcls, clsname, bases, clsdict)


class Stock(metaclass=DebugMeta):
    name = SizedString("name", size=8)
    shares = UnsignedInteger("shares")
    price = UnsignedFloat("price")

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


# name: <__main__.SizedString object at 0x7f84cc2241d0>
# shares: <__main__.UnsignedInteger object at 0x7f84cc224990>
# price: <__main__.UnsignedFloat object at 0x7f84cc2249d0>
# __init__: <function Stock.__init__ at 0x7f84cc211800>
