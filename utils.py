from numpy import array


def v(*args, **kwargs):
    return array(args, **kwargs)


def is_in(start, end, point):
    start_x, start_y = start
    end_x, end_y = end
    x, y = point
    return (start_x <= x < end_x) and (start_y <= y < end_y)


class Matrix:
    def __init__(self, *rows):
        self._rows = rows
        self.size = v(len(rows), len(rows[0]))
        for index, row in enumerate(rows):
            if len(row) != self.size[1]:
                raise ValueError('All arguments should be of an equal length:' \
                                 'argument {index} and 0 are not the same length.')

    def __getitem__(self, item):
        x, y = item
        return self._rows[y][x]

    def __setitem__(self, item, value):
       x, y = item
       self._rows[y][x] = value

class PaletteMatrix(Matrix):
    def __init__(self, palette, *rows):
        super().__init__(*rows)
        self.palette = palette

    def __getitem__(self, item):
        x, y = item
        return self.palette[super().__init__(item)]

