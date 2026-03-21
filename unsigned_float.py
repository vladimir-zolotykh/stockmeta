#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


class UnsignedFloat:
    def __init__(self):
        self._name = None

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if not isinstance(value, float):
            raise TypeError(f"{value}: must be of type float")
        if value < 0.0:
            raise ValueError(f"{value}: must be 0.0 or positive")
        instance.__dict__[self._name] = value


class Circle:
    radius = UnsignedFloat()


def test_UnsignedFloat():
    circle = Circle()
    circle.radius = 10.2
    assert circle.radius == 10.2
    x = -3.0
    with pytest.raises(ValueError) as exc:
        circle.radius = x
    assert str(exc.value) == f"{x}: must be 0.0 or positive"
