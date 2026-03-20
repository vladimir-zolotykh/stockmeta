#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Descriptor:
    def __init__(self):
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
    _required_type = type(None)

    def __set__(self, instance, val):
        if not isinstance(val, self._required_type):
            raise TypeError()
        super().__set__(instance, val)


class Bounded(Descriptor):
    def __init__(self, min_val=0, max_val=None):
        self.min_val = min_val
        self.max_val = max_val

    def __set__(self, instance, val):
        if not (val >= self.min_val and val <= self.max_val):
            raise ValueError()


class Integer(Typed):
    _required_type = int


class Unsigned(Bounded):
    def __init__(self):
        super().__init__(0, None)


class Float(Typed):
    _required_type = float


class UnsignedInteger(Integer, Unsigned):
    pass


class UnsignedFloat(Float, Unsigned):
    pass


class String(Typed):
    _required_type = str


class SizedString(String, Bounded):
    def __init__(self, min_len: int, max_len: int):
        super(String, self).__init__(min_len, max_len)


class Stock:
    name = SizedString(8)
    shares = UnsignedInteger()
    price = UnsignedFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


if __name__ == "__main__":
    s = Stock("ACME", 50, 91.1)
    s.shares = 97
    s.shares = -10
