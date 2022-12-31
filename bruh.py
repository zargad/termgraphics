#!/usr/bin/env python3
# -*- coding: ascii -*-
""""""
__author__ = 'Wak Man'


def main():
    Pixel(0x3983AA).display()


def parse(func):
    def wrapper(self, *args, **kwargs):
        generator = func(self, *args, **kwargs)
        return type(self)(*generator)
    return wrapper


class Color:
    def set_background(self):
        raise NotImplementedError

    def set_foreground(self):
        raise NotImplementedError


class RGB:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __iter__(self):
        yield self.red
        yield self.green
        yield self.blue

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
        pre_colors = RGB._get_pre_colors(hue, c, x)
        red, green, blue = map(lambda color: int((color + m) * 255), pre_colors)
        return cls(red, green, blue)

    @staticmethod
    def _get_pre_colors(hue, c, x):
        if 0 <= hue < 60:
            return c, x, 0
        elif 60 <= hue < 120:
            return x, c, 0
        elif 120 <= hue < 180:
            return 0, c, x
        elif 180 <= hue < 240:
            return 0, x, c
        elif 240 <= hue < 300:
            return x, 0, c
        elif 300 <= hue < 360:
            return c, 0, x

    def set_background(self):
        print('\033[48;2', *self, sep=';', end='m')

    def set_foreground(self):
        print('\033[38;2', *self, sep=';', end='m')

    @parse
    def __mul__(self, other):
        for i in self:
            yield int(i * other)

    @parse
    def __add__(self, other):
        for i, j in zip(self, other):
            yield i + j

    @parse
    def __sub__(self, other):
        for i, j in zip(self, other):
            yield i - j

    @parse
    def __floordiv__(self, other):
        for i in self:
            yield int(i / other)

    @parse
    def get_opposite_color(self):
        for i in self:
            yield 256 - i

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


basic_colors = {
    'white':   RGB.from_int(0xFFFFFF),
    'silver':  RGB.from_int(0xC0C0C0),
    'gray':    RGB.from_int(0x808080),
    'black':   RGB.from_int(0x000000),
    'red':     RGB.from_int(0xFF0000),
    'maroon':  RGB.from_int(0x800000),
    'yellow':  RGB.from_int(0xFFFF00),
    'olive':   RGB.from_int(0x808000),
    'lime':    RGB.from_int(0x00FF00),
    'green':   RGB.from_int(0x008000),
    'aqua':    RGB.from_int(0x00FFFF),
    'teal':    RGB.from_int(0x008080),
    'blue':    RGB.from_int(0x0000FF),
    'navy':    RGB.from_int(0x000080),
    'fuchsia': RGB.from_int(0xFF00FF),
    'purple':  RGB.from_int(0x800080),
}


class Pixel:
    def __init__(self, color, alpha=1.0, string=' '):
        self.color = RGB.from_generic(color)
        self.alpha = alpha
        self.string = string

    def display(self):
        self.color.set_background()
        print(self.string, end='')

    def __add__(self, other):
        color = self.color + (other.color - self.color) * other.alpha
        alpha = self.alpha + other.alpha
        if alpha > 1:
            alpha = 1
        return type(self)(color, alpha, other.string)

    def __or__(self, other):
        return type(self)(self.color, self.alpha, other)

    def __repr__(self):
        return f'Pixel({self.color!r}, {self.alpha!r}, {self.string!r})'


transparent = Pixel(0x000000, 0.0, '')

if __name__ == '__main__':
    main()
