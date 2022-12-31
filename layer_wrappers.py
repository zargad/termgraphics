# -*- coding: ascii -*-
from utils import is_in
from pixels import Pixel
from layers import Layer


class LayerWrapper(Layer):
    def __init__(self, wrapped_layer):
        self.wrapped_layer = wrapped_layer


class Box(LayerWrapper):
    def __init__(self, wrapped_layer, start, end):
        super().__init__(wrapped_layer)
        self.start = start
        self.end = end

    def get_pixel(self, point):
        if is_in(self.start, self.end, point):
            return self.wrapped_layer.get_pixel(point)
        return Pixel()

    def display(self, start=None, end=None):
        super().display(self.start if start is None else start, self.end if end is None else end)


class Transform(LayerWrapper):
    def __init__(self, wrapped_layer, func):
        super.__init__(wrapped_layer)
        self.func = func

    def get_pixel(self, point):
        return self.wrapped_layer.get_pixel(self.func(point))


class Stretch(LayerWrapper):
    def __init__(self, wrapped_layer, amount):
        super().__init__(wrapped_layer)
        self.amount = amount

    def get_pixel(self, point):
        return self.wrapped_layer.get_pixel(point // amount)


class Move(LayerWrapper):
    def __init__(self, wrapped_layer, amount):
        super().__init__(wrapped_layer)
        self.amount = amount

    def get_pixel(self, point):
        return self.wrapped_layer.get_pixel(point - amount)

