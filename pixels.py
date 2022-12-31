# -*- coding: ascii -*-
""""""
from colors import RGB


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
        self.color.set_background()
        super().display(char)

    def rcomposite(self, other):
        opaqueness = 1-(1-self.opaqueness)*(1-other.opaqueness)
        color = (self.color*self.opaqueness+other.color*(1-self.opaqueness))//opaqueness
        return RGBA(color, opaqueness)

    def composite(self, other):
        return other.rcomposite(self)

