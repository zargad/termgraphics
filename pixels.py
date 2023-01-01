# -*- coding: ascii -*-
""""""


class Pixel:
    def display(self, text=' '):
        print(text, end='\033[0m')

    def rcomposite(self, other):
        return other

    def composite(self, other):
        return other


class CharPixel(Pixel):
    def __init__(self, char):
        self.char = char

    def display(self):
        super().display(self.char)

    def rcomposite(self, other):
        return self

    def composite(self, other):
        return other.rcomposite(self)


class RGBA(Pixel):
    def __init__(self, color, opaqueness=1):
        self.color = color
        self.opaqueness = opaqueness

    def display(self, char=' '):
        self.set_background()
        super().display(char)

    def set_background(self):
        print('\033[48;2', *self.color, sep=';', end='m')

    def set_foreground(self):
        print('\033[38;2', *self.color, sep=';', end='m')

    def rcomposite(self, other):
        transparancy = 1 - self.opaqueness
        opaqueness = self.opaqueness + other.opaqueness * transparancy
        color = (int((i*self.opaqueness+j*transparancy)/opaqueness) for i,j in zip(self.color, other.color))
        return RGBA((*color, ), opaqueness)

    def composite(self, other):
        return other.rcomposite(self)

