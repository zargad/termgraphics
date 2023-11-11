# -*- encode: utf-8 -*-
"""Helper functions and classes for various modules in the library."""


def move_cursor(point):
    """Move the terminal cursor to a position from a two dimentional point."""
    print('\033[', end='')
    print(*point, sep=';', end='H')


def range_list(*ranges):
    return list(map(range, ranges))


def range_tuple(*ranges):
    return tuple(map(range, ranges))


class Matrix:
    """Array structure that can be indexed with a two dimentional point."""

    def __init__(self, *rows):
        self._rows = rows
        self.size = (range(len(rows)), range(len(rows[0])))
        for index, row in enumerate(rows):
            if len(row) != len(rows[0]):
                raise ValueError('All arguments should be of an equal length:' \
                        f'argument {index} and 0 are not the same length.')

    def __getitem__(self, item):
        x, y = item
        x_size, y_size = self.size
        if x in x_size and y in y_size:
            return self._rows[x][y]
        return None

    def __setitem__(self, item, value):
        x, y = item
        self._rows[y][x] = value


class PaletteMatrix(Matrix):
    """The data is stored in a dict and the keys are stored in the matrix"""
    # pylint: disable=too-few-public-methods

    def __init__(self, *rows, **palette):
        super().__init__(*rows)
        self.palette = palette

    def get_palette(self, item):
        return super().__getitem__(item)

    def __getitem__(self, item):
        index = self.get_palette(item)
        return None if index is None else self.palette[index]
