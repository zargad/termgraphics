# -*- coding: utf-8 -*-
"""Classes that inherit from LayerNode."""
from operator import floordiv, mul, sub
from layers import Layer


class LayerWrapper(Layer):
    """A Layer that wraps another Layer's functionality."""

    def __init__(self):
        super().__init__()
        self.wrapped_layer = None

    def get_pixel(self, point):
        get_pixel = self.wrapped_layer.get_pixel
        return self.get_wrapped_pixel(get_pixel, point)

    def get_wrapped_pixel(self, get_pixel, point):
        raise NotImplementedError

    def __radd__(self, other):
        self.wrapped_layer = other
        return self


class LayerChain(LayerWrapper):
    def __init__(self, base, **wrappers):
        self.wrapped_layer = base
        for wrapper in wrappers.values():
            self.wrapped_layer += wrapper
        self.tags = list(reversed(wrappers.keys()))
        self.tags.append('base')

    def get_layer(self, tag):
        index = self.tags.index(tag)
        layer = self.wrapped_layer
        for _ in range(index):
            layer = layer.wrapped_layer
        return layer

    def get_wrapped_pixel(self, get_pixel, point):
        return get_pixel(point)


class Box(LayerWrapper):
    """Return only the pixels within a specific range."""

    def __init__(self, range2d):
        super().__init__()
        self.range2d = range2d

    def get_wrapped_pixel(self, get_pixel, point):
        x, y = point
        range_x, range_y = self.range2d
        if x in range_x and y in range_y:
            return get_pixel(point)
        return None

    def display_print(self, range2d=None):
        if range2d is None:
            range2d = self.range2d
        super().display_print(range2d)


class Tile(LayerWrapper):
    """Return only the pixels within a specific range."""

    def __init__(self, range2d):
        super().__init__()
        self.size = range2d

    def get_wrapped_pixel(self, get_pixel, point):
        x, y = point
        size_x, size_y = self.size
        point = (x % size_x, y % size_y)
        return get_pixel(point)


class Transform(LayerWrapper):
    """Apply a function to the point argument of 'get_pixel' before returning the pixel."""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs

    def transform(self, point, *args, **kwargs):
        """Transform a point to another one."""
        raise NotImplementedError

    def get_wrapped_pixel(self, get_pixel, point):
        return get_pixel(tuple(self.transform(point, *self.args, **self.kwargs)))


class LambdaTransform(Transform):
    """Get the transformation function from the constructor."""

    def __init__(self, func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.func_ = func

    def transform(self, point, *args, **kwargs):
        return self.func_(point, *args, **kwargs)


class TransformBoth(LambdaTransform):
    """Apply the same function to the both coordinates of the point in get_pixel."""

    def __init__(self, func, *args, **kwargs):
        super().__init__(func, *args)

    def transform(self, point, *args, **kwargs):
        for coordinate, *args in zip(point, *args):
            yield super().transform(coordinate, *args)


class Stretch(TransformBoth):
    """Stretch a Layer by an amount."""

    def __init__(self, amount):
        super().__init__(floordiv, amount)


class Compress(TransformBoth):
    """Compress a Layer by an amount."""
    def __init__(self, amount):
        super().__init__(mul, amount)


class Move(TransformBoth):
    """Offset a Layer by an amount."""
    def __init__(self, amount):
        super().__init__(sub, amount)
