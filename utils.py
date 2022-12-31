from numpy import array


def v(*args, **kwargs):
    return array(args, **kwargs)


def is_in(start, end, point):
    return all(start <= point) and all(point < end)


def parse(method):
    def wrapper(self, *args, **kwargs):
        fields = method(self, *args, **kwargs)
        return type(self)(*fields)
    return wrapper


class Matrix:
    def __init__(self, *rows):
        self._rows = rows
        self.size = v(len(rows), len(rows[0]))
        for index, row in enumerate(rows):
            if len(row) != self.size[1]:
                raise ValueError('All arguments should be of an equal length: argument {index} and 0 are not the same length.')

    def __getitem__(self, item):
        x, y = item
        return self._rows[y][x]

    # def __setitem__(self, item, value):
    #    x, y = item
    #    self._rows[y][x] = value

