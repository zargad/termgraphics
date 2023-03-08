# -*- coding: utf-8 -*-
"""Classes that inherit from Pixel."""


class Pixel:
    """Able to be added and displayed."""

    def __init__(self, opaqueness=0):
        self.opaqueness = opaqueness

    def __bool__(self):
        return bool(self.opaqueness)

    def __imul__(self, x):
        self.opaqueness *= x

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
        super().__init__()
        self.char = char

    def display(self):
        print(self.char, end='\033[0m')

    def __radd__(self, other):
        return self


class RGBA(Pixel):
    """Displays a color and added with alpha compositing."""

    def __init__(self, color, opaqueness=1):
        super().__init__()
        self.color = color
        self.opaqueness = opaqueness

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
