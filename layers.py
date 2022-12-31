from utils import is_in, Matrix, v
from pixels import Pixel


class Layer:
    def display(self, start, end):
        start_x, start_y = start
        end_x, end_y = end
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                self.get_pixel(v(x, y)).display()
            print()

    def get_pixel(self, point):
        raise NotImplementedError

    def wrap(self, wrapper, *args, **kwargs):
        return wrapper(self, *args, **kwargs)


class NArrayLayer(Layer):
    def __init__(self, narray, convert_item):
        self.narray = narray
        self.convert_item = covert_item

    def get_pixel(self, point):
        self.narray[self.convert_item(point)]


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
        super().__init__()
        self._layers = args

    def get_pixel(self, point):
        pixel = Pixel()
        for layer in self._layers:
            bruh = layer.get_pixel(point)
            pixel = pixel.composite(bruh)
        return pixel
 
