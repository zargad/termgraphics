# -*- encode: utf-8 -*-
"""Classes that inherit from Layer."""
from typing import Self
from itertools import product
# from multiprocessing import Pool
from utils import move_cursor


class Layer:
    """Can get Pixels from two dimentional points and display them in a grid."""
    def __init__(self):
        self.tag_ = None

    def get_layer_by_path(self, path, seperator='.'):
        tags = path.split(seperator)
        return self.get_layer(*tags)

    def display_print(self, range2d):
        """Displays the Pixels in a grid from two ranges."""
        for point in product(*range2d):
            x, y = point
            move_cursor((x + 1, y + 1))
            pixel = self.get_pixel(point)
            pixel.display()
            #print()

    def get_pixel(self, point):
        """Get a Pixel from a point."""
        raise NotImplementedError

    def tag(self, tag_):
        self.tag_ = tag_
        return self

    def get_layer(self, *tags):
        if not tags:
            return self
        sub_layer = self.get_sub_layer(*tags)
        if sub_layer is None:
            raise KeyError(f'{self} does not contain a Layer with the tags: {tags}.')
        return sub_layer

    def get_sub_layer(self, current_tag, *tags) -> Self | None:
        return None


class Image(Layer):
    """Get pixels from a matrix."""

    def __init__(self, matrix):
        self.matrix = matrix

    def get_pixel(self, point):
        return self.matrix[point]


class PixelLayer(Layer):
    """Return the same Pixel for every point."""

    def __init__(self, pixel):
        super().__init__()
        self.pixel = pixel

    def get_pixel(self, point):
        return self.pixel


class LayerPile(Layer):
    """Contains a list of layers and returs the addition of their pixels."""

    def __init__(self, **layers):
        super().__init__()
        self.layers = [layer.tag(tag_) for (tag_, layer) in layers.items()]

    def get_sub_layer(self, current_tag, *tags):
        for layer in self.layers:
            if layer.tag_ == current_tag:
                return layer.get_layer(*tags)
        return None

    def get_pixel(self, point):
        layer, *layers = self.layers
        final_pixel = layer.get_pixel(point)
        for layer in layers:
            current_pixel = layer.get_pixel(point)
            final_pixel += current_pixel
        return final_pixel


# class BufferLayer(Image):
#     def __init__(self, size):
#         x, y = size
#         super().__init__([[None for __ in range(x)] for _ in range(y)])
#         self.size = size
#
#     def clear():
#         pass
#
#     def append():
#         pass
