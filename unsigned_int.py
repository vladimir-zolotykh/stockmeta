#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


class UnsignedInteger:
    def __init__(self):
        self._name = None

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"{value}: must be of type int")
        if value < 0:
            raise ValueError(f"{value}: must be non negative")
        instance.__dict__[self._name] = value


class Person:
    age = UnsignedInteger()


# def test_UnsignedFloat():
def test_UnsignedInteger():
    p = Person()
    p.age = 35
    assert p.age == 35
    with pytest.raises(TypeError) as exc:
        p.age = (s := "old")
    assert str(exc.value) == f"{s}: must be of type int"
    with pytest.raises(ValueError) as exc:
        p.age = (x := -3)
    assert str(exc.value) == f"{x}: must be non negative"
