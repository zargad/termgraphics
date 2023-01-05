# -*- coding: ascii -*-
from operator import floordiv, mul, sub
from utils import is_in
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
        return None

    def display(self, start=None, end=None):
        start = self.start if start is None else start
        end = self.end if end is None else end
        super().display(start, end)


class Transform(LayerWrapper):
    def __init__(self, wrapped_layer, func, *constants):
        super().__init__(wrapped_layer)
        self._func = func
        self.constants = constants

    def func(self, point):
        return self._func(point, *self.constants)

    def get_pixel(self, point):
        return self.wrapped_layer.get_pixel(self.func(point))


class TransformBoth(Transform):
    def func(self, point):
        return tuple(self._func(i, *self.constants) for i in zip(point, self.constants))


class Stretch(TransformBoth):
    def __init__(self, wrapped_layer, amount):
        super().__init__(wrapped_layer, floordiv, amount)


class Compress(TransformBoth):
    def __init__(self, wrapped_layer, amount):
        super().__init__(wrapped_layer, mul, amount)


class Move(TransformBoth):
    def __init__(self, wrapped_layer, amount):
        super().__init__(wrapped_layer, sub, amount)

