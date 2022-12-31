#!/usr/bin/env python3
# -*- coding: ascii -*-
""""""
from numpy import ndarray
from utils import v, parse


class Color:
    def set_background(self):
        raise NotImplementedError

    def set_foreground(self):
        raise NotImplementedError


class RGB(Color, ndarray):
    def __init__(red, green, blue):
        super().__init__((red, green, blue))

    @classmethod
    def from_generic(cls, value):
        if isinstance(value, (cls, tuple, list)):
            return cls(*value)
        elif isinstance(value, int):
            return cls.from_int(value)
        else:
            raise TypeError

    @classmethod
    def from_int(cls, n):
        blue = n % 256
        n >>= 8
        green = n % 256
        n >>= 8
        red = n % 256
        return cls(red, green, blue)

    @classmethod
    def from_hsv(cls, hue=0, saturation=1, value=1):
        hue_ = (hue / 60)
        c = value * saturation
        x = c * (1 - abs(hue_ % 2 - 1))
        m = value - c
        pre_colors = RGB._get_pre_colors(hue_, c, x)
        red, green, blue = map(lambda color: int((color + m) * 255), pre_colors)
        return cls(red, green, blue)

    @staticmethod
    def _get_pre_colors(hue_, c, x):
        return ((c, x, 0),
                (x, c, 0),
                (0, c, x),
                (0, x, c),
                (x, 0, c),
                (c, 0, x))[int(hue_)]

    def set_background(self):
        print('\033[48;2', *self, sep=';', end='m')

    def set_foreground(self):
        print('\033[38;2', *self, sep=';', end='m')

    def __int__(self):
        return self.red + self.green * 256 + self.blue * 256 ** 2

    def __repr__(self):
        return f'RGB({self.red!r}, {self.green!r}, {self.blue!r})'

    def __format__(self, format_spec):
        if format_spec == 'b':
            ansi_code = '48'
        elif format_spec == 'f':
            ansi_code = '38'
        else:
            raise ValueError
        return f'\033[{ansi_code};2;{self.red};{self.green};{self.blue}m'

