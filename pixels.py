# -*- coding: utf-8 -*-
"""Classes that inherit from Pixel."""


class Pixel:
    """Able to be added and displayed."""

    def __bool__(self):
        return False

    def display(self):
        """Display to the console."""
        raise NotImplementedError

    def __add__(self, other):
        if other:
            return other.__radd__(self)
        return self

    def __radd__(self, other):
        return other


class CharPixel(Pixel):
    """Displays a colorless character."""

    def __init__(self, char):
        self.char = char

    @property
    def char(self):
        return self._char

    @char.setter
    def char(self, value):
        if len(value) != 1:
            raise ValueError('char is one character long')
        self._char = value
        self.is_opaque = not value.isspace()

    def __bool__(self):
        return self.is_opaque

    def display(self):
        print(self.char, end='\033[0m')

    def __radd__(self, other):
        return self


class RGBA(Pixel):
    """Displays a color and added with alpha compositing."""

    def __init__(self, color, opaqueness=1):
        self.color = color
        self.opaqueness = opaqueness

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if len(value) != 3:
            raise ValueError('color should be the length of 3')
        for i in value:
            if not 0 <= i < 256:
                raise ValueError('all values in color should be between 0 and 255')
        self._color = value

    @property
    def opaqueness(self):
        return self._opaqueness

    @opaqueness.setter
    def opaqueness(self, value):
        if not 0 <= value <= 1:
            raise ValueError('opaqueness should be between 0 and 1')
        self._opaqueness = value


    def __bool__(self):
        return bool(self.opaqueness)

    @classmethod
    def from_hex(cls, hex_number):
        opaqueness = (hex_number % 256) / 256
        hex_mumber = hex_number >> 8
        red = hex_number % 256
        hex_mumber = hex_number >> 8
        green = hex_number % 256
        hex_mumber = hex_number >> 8
        blue = hex_number % 256
        return cls((red, green, blue), opaqueness)

    def display(self):
        self.set_background()
        print(' ', end='\033[0m')

    def set_background(self):
        """Print to the console the ansi escape code to color the background with self.color."""
        print('\033[48;2', *self.color, sep=';', end='m')

    def set_foreground(self):
        """Print to the console the ansi escape code to color the foreground with self.color."""
        print('\033[38;2', *self.color, sep=';', end='m')

    def __radd__(self, other):
        transparancy = 1 - self.opaqueness
        opaqueness = self.opaqueness + other.opaqueness * transparancy
        color = (int((i*self.opaqueness+j*transparancy)/opaqueness)
                 for i, j in zip(self.color, other.color))
        return RGBA((*color, ), opaqueness)

    class Invert:
        def __radd__(self, other):
            color = map(lambda i: 255 - i, other.color)
            opaqueness = other.opaqueness
            return type(other)((*color, ), opaqueness)

    class Multiply:
        def __init__(self, coefficients):
            self.coefficients = coefficients

        def __radd__(self, other):
            color = (a*c for (a, c) in zip(self.coefficients, other.color))
            opaqueness = other.opaqueness
            return type(other)((*color, ), opaqueness)


Colors = {
    'black': RGBA.from_hex(0x000000FF),
    'red': RGBA.from_hex(0xFF0000FF),
    'yellow': RGBA.from_hex(0xFFFF00FF),
    'green': RGBA.from_hex(0x00FF00FF),
    'cyan': RGBA.from_hex(0x00FFFFFF),
    'blue': RGBA.from_hex(0x0000FFFF),
    'magenta': RGBA.from_hex(0xFF00FFFF),
}
