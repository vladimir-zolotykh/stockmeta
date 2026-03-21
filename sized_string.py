#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


class SizedString:
    def __init__(self, min_len: int, max_len: int):
        self.min_len = min_len
        self.max_len = max_len
        self._name = None

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, val: str):
        if not isinstance(val, str):
            raise TypeError(f"{val} must be str")
        if len(val) < self.min_len or len(val) > self.max_len:
            raise ValueError(
                f"{val}: length must be in range [{self.min_len}..{self.max_len}]"
            )
        instance.__dict__[self._name] = val


class Product:
    name = SizedString(1, 8)


def test_SizedString():
    item = Product()
    item.name = "Widget"
    assert item.name == "Widget"
    x = 10
    with pytest.raises(TypeError) as exc:
        item.name = x
    assert str(exc.value) == f"{x!r} must be str"
    s = "ABRACADABRA"
    with pytest.raises(ValueError) as exc:
        item.name = s
    # assert str(exc.value) == f"{s}: length must be in range [1..8]"
    assert str(exc.value) == "{}: length must be in range [{}..{}]".format(
        s, Product.name.min_len, Product.name.max_len
    )
