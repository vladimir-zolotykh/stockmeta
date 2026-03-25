#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


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


class TypedDeco:
    def __init__(self, expected_type=None):
        self._expected_type = expected_type

    def __call__(self, cls):  # change ``self'' to ``cls''
        super_set = cls.__set__

        def __set__(descriptor, instance, value):
            if not isinstance(value, self._expected_type):
                raise TypeError(f"{value} must be of type {self._expected_type}")
            super_set(descriptor, instance, value)

        cls.__set__ = __set__
        return cls


def Unsigned(cls):
    super_set = cls.__set__

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"{value} must be positive")
        super_set(self, instance, value)

    cls.__set__ = __set__
    return cls


@TypedDeco(int)
class Integer(Descriptor):
    pass


@TypedDeco(float)
class Float(Descriptor):
    pass


@TypedDeco(float)
@Unsigned
class UnsignedFloat(Descriptor):
    pass


class Stock:
    shares = Integer()
    price = Float()
    price = UnsignedFloat()

    def __init__(self, shares, price):
        self.shares = shares
        self.price = price


@pytest.fixture
def stock():
    return Stock(50, 91.1)


def test_shares(stock):
    assert stock.shares == 50
    with pytest.raises(TypeError) as exc:
        stock.shares = (x := 90.1)
    assert str(exc.value) == f"{x} must be of type <class 'int'>"


def test_price(stock):
    assert stock.price == 91.1
    with pytest.raises(TypeError) as exc:
        stock.price = (x := "too expensive")
    assert str(exc.value) == f"{x} must be of type <class 'float'>"
    with pytest.raises(ValueError) as exc:
        stock.price = (x := -10.3)
    assert str(exc.value) == f"{x} must be positive"


if __name__ == "__main__":
    import sys

    pytest.main(sys.argv)
