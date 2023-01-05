from multiprocessing import Pool
from utils import is_in, Matrix


class Layer:
    def display(self, start, end):
        start_x, start_y = start
        end_x, end_y = end
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                print('\033[', end='')
                print(y, x, sep=';', end='H')
                self.get_pixel((x, y)).display()
            #print()

    def get_pixel(self, point):
        raise NotImplementedError

    def wrap(self, wrapper, *args, **kwargs):
        return wrapper(self, *args, **kwargs)


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

