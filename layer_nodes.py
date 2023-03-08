# -*- coding: utf-8 -*-
"""Classes that inherit from LayerNode."""
from operator import floordiv, mul, sub
from layers import Layer


class LayerNode(Layer):
    """Layer that can be nested and be given from a collection of tags."""

    def __init__(self):
        super().__init__()
        self.tag_ = None

    def tag(self, tag):
        """Set the tag."""
        self.tag_ = tag
        return self

    def is_tagged(self, tag):
        """Get whether the layer is tagged or not."""
        return tag == self.tag_

    def get_layer(self, current_tag, *tags):
        """Get a nested layer from a collection of tags."""
        raise NotImplementedError


class LayerWrapper(LayerNode):
    """A Layer that wraps another Layer's functionality."""

    def __init__(self):
        super().__init__()
        self.wrapped_layer = None

    def get_layer(self, current_tag, *tags):
        if self.is_tagged(current_tag):
            return self.wrapped_layer.get_layer(*tags) if tags else self.wrapped_layer
        return None

    def __radd__(self, other):
        self.wrapped_layer = other
        return self


class TaggedLayer(LayerWrapper):
    """Returns the pixel without modifying it but adds a tag to the class."""

    def __init__(self, tag):
        super().__init__()
        self.tag(tag)

    def get_pixel(self, point):
        return self.wrapped_layer.get_pixel(point)


class LayerPile(LayerNode):
    """Contains a list of layers and returs the addition of their pixels."""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.layers = [v + TaggedLayer(k) for (k, v) in kwargs.items()]
        self.layers.extend(args)

    def get_layer(self, current_tag, *tags):
        if self.is_tagged(current_tag):
            next_tag, *tags = tags
            for layer in self.layers:
                if layer.is_tagged(next_tag):
                    return layer.get_layer(*tags) if tags else layer
        return None

    def get_pixel(self, point):
        layer, *layers = self.layers
        final_pixel = layer.get_pixel(point)
        for layer in layers:
            current_pixel = layer.get_pixel(point)
            final_pixel += current_pixel
        return final_pixel


class Box(LayerWrapper):
    """Return only the pixels within a specific range."""

    def __init__(self, range2d):
        super().__init__()
        self.range2d = range2d

    def get_pixel(self, point):
        x, y = point
        range_x, range_y = self.range2d
        if x in range_x and y in range_y:
            return self.wrapped_layer.get_pixel(point)
        return None

    def display_print(self, range2d=None):
        if range2d is None:
            range2d = self.range2d
        super().display_print(range2d)


class Transform(LayerWrapper):
    """Apply a function to the point argument of 'get_pixel' before returning the pixel."""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs

    def transform(self, point, *args, **kwargs):
        """Transform a point to another one."""
        raise NotImplementedError

    def get_pixel(self, point):
        return self.wrapped_layer.get_pixel(self.transform(point, *self.args, **self.kwargs))


class LambdaTransform(Transform):
    """Get the transformation function from the constructor."""

    def __init__(self, func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.func_ = func

    def transform(self, point, *args, **kwargs):
        return self.func_(point, *args, **kwargs)


class TransformBoth(LambdaTransform):
    """Apply the same function to the both coordinates of the point in get_pixel."""

    def __init__(self, func, *args, **kwargs):  # TODO **kwargs
        super().__init__(func, *args)

    def transform(self, point, *args, **kwargs):  # TODO **kwargs
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
