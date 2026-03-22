#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


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
        self.validate(instance, value)
        instance.__dict__[self._name] = value

    def validate(self, instance, value):
        return value


class Typed(Descriptor):
    _type = type(None)

    def validate(self, instance, value):
        if not isinstance(value, self._type):
            raise TypeError(f"{value}: expected {self._type}")
        super().validate(instance, value)


class Integer(Typed):
    _type = int


class Float(Typed):
    _type = float


class String(Typed):
    _type = str


class Unsigned(Descriptor):
    def validate(self, instance, value):
        if value < 0:
            raise ValueError(f"{value}: must be non negative")
        super().validate(instance, value)


class UnsignedInteger(Integer, Unsigned):
    pass


class UnsignedFloat(Float, Unsigned):
    pass


class Bounded(Descriptor):
    def validate(self, instance, value):
        if len(value) < self.min_len or len(value) > self.max_len:
            raise ValueError(
                f"{value}: value must be in range [{self.min_len}..{self.max_len}]"
            )
        super().validate(instance, value)


class SizedString(String, Bounded):
    def __init__(self, **opt):
        if "min_len" not in opt:
            opt["min_len"] = 0
        if "max_len" not in opt:
            raise ValueError("max_len is missing")
        super().__init__(**opt)


class Stock:
    name = SizedString(max_len=12)
    shares = UnsignedInteger()
    price = UnsignedFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


@pytest.fixture
def stock():
    return Stock("ACME", 50, 91.1)


def test_stock_10(stock):
    s = stock
    assert s.shares == 50
    assert s.name == "ACME"
    assert s.price == 91.1


def test_stock_20(stock):
    s = stock
    with pytest.raises(ValueError) as exc:
        s.shares = (x := -10)
    assert str(exc.value) == f"{x}: must be non negative"


def test_stock_30(stock):
    s = stock
    s.name = "ABRA"
    assert s.name == "ABRA"


def test_stock_40(stock):
    s = stock
    with pytest.raises(ValueError) as exc:
        s.name = (t := "ABRACADABRAABRACAD")
    assert str(exc.value) == f"{t}: value must be in range [0..12]"


def test_stock_50(stock):
    s = stock
    with pytest.raises(TypeError) as exc:
        s.shares = (t := "too much")
    assert str(exc.value) == f"{t}: expected <class 'int'>"
