# -*- coding: ascii -*-
from operator import floordiv, mul, sub
from layers import Layer


class LayerNode(Layer):
    def __init__(self):
        self._tag = ''

    def tag(self, tag):
        self._tag = tag
        return self

    def get_layer(self, current_tag, *tags):
        return NotImplementedError


class LayerWrapper(LayerNode):
    def __init__(self):
        super().__init__()
        self.wrapped_layer = None

    def get_layer(self, current_tag, *tags):
        if current_tag == self._tag:
            return self.wrapped_layer.get_layer(*tags) if tags else self.wrapped_layer
        return None
        
    def __radd__(self, other):
        self.wrapped_layer = other
        return self


class TaggedLayer(LayerWrapper):
    def __init__(self, tag):
        self._tag = tag

    def get_pixel(self, point):
        return self.wrapped_layer.get_pixel(point)


class LayerPile(LayerNode):
    def __init__(self, *args, **kwargs):
        self.layers = [v + TaggedLayer(k) for (k, v) in kwargs.items()]
        self.layers.extend(args)

    def get_layer(self, current_tag, *tags):
        if current_tag == self._tag:
            next_tag = tags.pop(0)
            for layer in self.layers:
                if next_tag == layer._tag:
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
    def __init__(self, range2d):
        super().__init__()
        self.range2d = range2d

    def get_pixel(self, point):
        x, y = point
        range_x, range_y = self.range2d
        if x in range_x and y in range_y:
            return self.wrapped_layer.get_pixel(point)
        return None

    def display(self, range2d=None):
        if range2d is None:
            range2d = self.range2d
        super().display(range2d)


class Transform(LayerWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs

    def func(self, point, *args, **kwargs):
        raise NotImplementedError

    def get_pixel(self, point):
        return self.wrapped_layer.get_pixel(self.func(point, *self.args, **self.kwargs))


class LambdaTransform(Transform):
    def __init__(self, func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._func = func

    def func(self, point, *args, **kwargs):
        return self._func(point, *args, **kwargs)


class TransformBoth(LambdaTransform):
    def __init__(self, func, *args):
        super().__init__(func, *args)

    def func(self, point, *args):
        return tuple(self._func(i, *a) for i,*a in zip(point, *args))


class Stretch(TransformBoth):
    def __init__(self, amount):
        super().__init__(floordiv, amount)


class Compress(TransformBoth):
    def __init__(self, amount):
        super().__init__(mul, amount)


class Move(TransformBoth):
    def __init__(self, amount):
        super().__init__(sub, amount)

