from utils import is_in, v


class Layer:
    def display(self, start, end):
        start_x, start_y = start
        end_x, end_y = end
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                self.get_pixel(v(x, y)).display()
            print()

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
        super().__init__()
        self._layers = args

    def get_pixel(self, point):
        layer, *layers = self._layers
        final_pixel = layer.get_pixel(point)
        for layer in layers:
            current_pixel = layer.get_pixel(point)
            final_pixel = final_pixel.composite(current_pixel)
        return final_pixel
 

