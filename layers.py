from itertools import product
from multiprocessing import Pool
from utils import is_in, Matrix, move_cursor


class Layer:
    def display_print(self, range2d):
        for point in product(*range2d):
            move_cursor(point)
            self.get_pixel(point).display()
            #print()

    def get_pixel(self, point):
        raise NotImplementedError


class Image(Layer):
    def __init__(self, matrix):
        self.matrix = matrix

    def get_pixel(self, point):
        return self.matrix[point]


class PixelLayer(Layer):
    def __init__(self, pixel):
        super().__init__()
        self.pixel = pixel

    def get_pixel(self, point):
        return self.pixel


class LayerPile(Layer):
    def __init__(self, *args):
        self._layers = args

    def get_pixel(self, point):
        layer, *layers = self._layers
        final_pixel = layer.get_pixel(point)
        for layer in layers:
            current_pixel = layer.get_pixel(point)
            final_pixel += current_pixel
        return final_pixel
 

class BufferLayer(Image):
    def __init__(self, size): 
        x, y = size
        super().__init__([[None for __ in range(x)] for _ in range(y)])
        self.size = size

    def clear():
        pass
    
    def append():
        pass

