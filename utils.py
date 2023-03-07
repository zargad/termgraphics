from numpy import array


def move_cursor(point):
    print('\033[', end='')
    print(*point, sep=';', end='H')


class Matrix:
    def __init__(self, *rows):
        self._rows = rows
        self.size = (range(len(rows)), range(len(rows[0])))
        for index, row in enumerate(rows):
            if len(row) != len(rows[0]):
                raise ValueError('All arguments should be of an equal length:' \
                                 'argument {index} and 0 are not the same length.')

    def __getitem__(self, item):
        x, y = item
        x_size, y_size = self.size
        if x in x_size and y in y_size: 
            return self._rows[x][y]
        return None

    def __setitem__(self, item, value):
       x, y = item
       self._rows[y][x] = value


class ListPaletteMatrix(Matrix):
    def __init__(self, palette, *rows):
        super().__init__(*rows)
        self.palette = palette

    def __getitem__(self, item):
        index = super().__getitem__(item)
        return None if index is None else self.palette[index]


class DictPaletteMatrix(Matrix):
    def __init__(self, *rows, **palette):
        super().__init__(*rows)
        self.palette = palette

    def __getitem__(self, item):
        index = super().__getitem__(item)
        return None if index is None else self.palette[index]

