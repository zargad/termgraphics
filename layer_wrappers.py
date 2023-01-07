# -*- coding: ascii -*-
from operator import floordiv, mul, sub
from utils import is_in
from layers import Layer
from re import match


# CompositeLayer


coel = LayerCollection(a=LayerCollection(b=Layer),c=Layer,b=Layer)


"""
class LayerCollection(Layer):
    def __init__(self, **layers):
        self.layers = layers

    def get_layer(self, tags):
        current_tag = tags.pop(0)
        current_layer = self.layers.get(current_tag)
        if tags:
            if isinstance(current_layer, LayerCollection):
                return current_layer.get_layer(tags)
            return None
        return current_layer

    def get_layer_regex(self, tags):
        current_tag = tags.pop(0)
        for tag, current_layer in self.layer.items():
            if match(current_tag, tag):
                if tags:
                    if isinstance(current_layer, LayerCollection):
                        return current_layer.get_layer(tags)
                    return None
                return current_layer
"""


class LayerNode(Layer):
    def __init__(self, tag):
        self.tag = tag

    def get_layer(self, *tags):
        raise NotImplementedError


class LayerWrapper(LayerNode):
    def __init__(self, tag=''):
        super().__init__(tag)
        self.wrapped_layer = None

    def get_layer(self, current_tag, *tags):
        if current_tag == self.tag:
            return self.wrapped_layer.get_layer(*tags) if tags else self.wrapped_layer
        return None
        
    def wrap_with(self, wrapper, *args, **kwargs):
        return wrapper(*args, **kwargs).wrap(self)

    def wrap(self, wrapped_layer):
        self.wrapped_layer = wrapped_layer


class Box(LayerWrapper):
    def __init__(self, range2d, tag=''):
        super().__init__(tag)
        self.range2d = range2d

    def get_pixel(self, point):
        x, y = point
        range_x, range_y = self.range2d
        if x in range_x and y in range_y:
            return self.wrapped_layer.get_pixel(point, **layers)
        return None

    def display(self, range2d=None):
        if range2d is None:
            range2d = self.range2d
        super().display(range2d)


class Transform(LayerWrapper):
    def __init__(self, *constants):
        self().__init__()
        self.constants = constants

    def func(self, point):
        raise NotImplementedError

    def get_pixel(self, point):
        return self.wrapped_layer.get_pixel(self.func(point))


class LambdaTransform(Transform):
    def __init__(self, func, *constants):
        super().__init__(*constants)
        self._func = func

    def func(self, point):
        return self._func(point, *self.constants)


class TransformBoth(LayerWrapper):
    def __init__(self, func, *constants):
        super().__init__(*constants)
        self._func = func

    def func(self, point):
        return tuple(self._func(i, *c) for i,*c in zip(point, *self.constants))


class Stretch(TransformBoth):
    def __init__(self, amount):
        super().__init__(floordiv, amount)


class Compress(TransformBoth):
    def __init__(self, amount):
        super().__init__(mul, amount)


class Move(TransformBoth):
    def __init__(self, amount):
        super().__init__(sub, amount)

