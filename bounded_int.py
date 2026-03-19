#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


class BoundedInt:
    def __init__(self, min_value=0, max_value=100):
        self.min_value = min_value
        self.max_value = max_value
        self._name = None

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"{value} must be int")
        if not (value >= self.min_value and value <= self.max_value):
            raise ValueError(f"{value} must be in [{self.min_value}, {self.max_value}(")
        instance.__dict__[self._name] = value


class Player:
    score = BoundedInt()


def test_BoundedInt():
    player = Player()
    val = -3
    with pytest.raises(ValueError) as exc:
        player.score = val
    assert str(exc.value) == f"{val} must be in [0, 100("
    player.score = 10
    assert player.score == 10
    val = 123
    with pytest.raises(ValueError) as exc:
        player.score = val
    assert str(exc.value) == f"{val} must be in [0, 100("


if __name__ == "__main__":
    import sys

    pytest.main(sys.argv)
