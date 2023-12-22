# -*- encode: utf-8 -*-
"""Classes that inherit from Layer."""
from typing import Self
from itertools import product
# from multiprocessing import Pool
from utils import move_cursor


class Layer:
    """Can get Pixels from two dimentional points and display them in a grid."""
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


class Image(Layer):
    """Get pixels from a matrix."""

    def __init__(self, matrix):
        self.matrix = matrix

    def get_pixel(self, point):
        return self.matrix[point]


class Tiles(Layer):
    """Get pixels from a matrix."""

    def __init__(self, size, matrix):
        self.size = size
        self.matrix = matrix

    def get_pixel(self, point):
        x, y = point
        size_x, size_y = self.size
        tile = self.matrix[(x // size_x, y // size_y)]
        if tile is None:
            return None
        return tile[(x % size_x, y % size_y)]


class UniformLayer(Layer):
    """Return the same Pixel for every point."""

    def __init__(self, pixel):
        super().__init__()
        self.pixel = pixel

    def get_pixel(self, point):
        return self.pixel


class LayerList(Layer):
    """Contains a list of layers and returs the addition of their pixels."""

    def __init__(self, *layers):
        super().__init__()
        self.layers = layers


class LayerPile(LayerList):
    """Contains a list of layers and returs the addition of their pixels."""
    def get_pixel(self, point):
        layer, *layers = self.layers
        final_pixel = layer.get_pixel(point)
        for layer in layers:
            current_pixel = layer.get_pixel(point)
            final_pixel += current_pixel
        return final_pixel


class LayerTilesVert(LayerList):
    """Contains a list of layers and returs the addition of their pixels."""

    def __init__(self, tile_length, *layers):
        super().__init__(*layers)
        self.tile_length

    def get_pixel(self, point):
        x, y = point
        index = x // self.tile_length
        if 0 <= index < len(self.layers):
            layer = self.layers[index]
            x %= self.tile_length
            point = (x, y)
            return layer.get_pixel(point)
        return None


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
