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


class TypedDeco:
    def __init__(self, expected_type=None):
        self._expected_type = expected_type

    def __call__(self, cls):
        super_set = cls.__set__

        def __set__(self, instance, value):
            if not isinstance(value, self._expected_type):
                raise TypeError(f"{value} must be of type {self._expected_type}")
            super_set(instance, value)

        cls.__set__ = __set__
        return cls


@TypedDeco(int)
class Integer(Descriptor):
    pass


class Stock:
    shares = Integer()

    def __init__(self, shares):
        self.shares = shares


if __name__ == "__main__":
    stock = Stock(50)
    print(stock.shares)
