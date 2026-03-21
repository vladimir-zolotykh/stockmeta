#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Descriptor:
    def __init__(self, **opt):
        for key, val in opt.items():
            setattr(self, key, val)
        self._name = None

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        instance.__dict__[self._name] = value


class Typed(Descriptor):
    _type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self._type):
            raise TypeError(f"{type(value)}: expected {self._type}")
        super().__set__(instance, value)


class Integer(Typed):
    _type = int


class Float(Typed):
    _type = float


class String(Typed):
    _type = str


class UnsignedInteger(Integer):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"{value}: must be non negative")
        super().__set__(instance, value)


class UnsignedFloat(Float):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"{value}: must be non negative")
        super().__set__(instance, value)


class SizedString(String):
    def __init__(self, **opt):
        if "min_len" not in opt:
            opt["min_len"] = 0
        if "max_len" not in opt:
            raise ValueError("max_len is missing")
        super().__init__(**opt)

    def __set__(self, instance, value):
        if len(value) < self.min_len or len(value) > self.max_len:
            raise ValueError(
                f"{value}: length must be in range [{self.min_len}..{self.max_len}]"
            )
        super().__set__(instance, value)


class Stock:
    name = SizedString(max_len=12)
    shares = UnsignedInteger()
    price = UnsignedFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


def test_stock():
    s = Stock("ACME", 50, 91.1)
    assert s.shares == 50
