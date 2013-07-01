class _has(object):
    def __init__(self, key):
        self._key = key

    def __eq__(self, other):
        self._value_eq = other
        return self

    def __lt__(self, other):
        self._value_lt = other
        return self

    def __le__(self, other):
        self._value_le = other
        return self

    def __gt__(self, other):
        self._value_gt = other
        return self

    def __ge__(self, other):
        self._value_ge = other
        return self

    def __or__(self, other):
        return _has_or(self, other)

    def __and__(self, other):
        return _has_and(self, other)

    def __call__(self, element):
        if self._key not in element:
            return False

        try:
            return element[self._key] == self._value_eq
        except AttributeError:
            pass

        try:
            return element[self._key] < self._value_lt
        except AttributeError:
            pass

        try:
            return element[self._key] <= self._value_le
        except AttributeError:
            pass

        try:
            return element[self._key] > self._value_gt
        except AttributeError:
            pass

        try:
            return element[self._key] >= self._value_ge
        except AttributeError:
            pass

has = _has


class _has_or(object):
    def __init__(self, where1, where2):
        self._cond_1 = where1
        self._cond_2 = where2

    def __call__(self, element):
        return self._cond_1(element) or self._cond_2(element)


class _has_and(object):
    def __init__(self, where1, where2):
        self._cond_1 = where1
        self._cond_2 = where2

    def __call__(self, element):
        return self._cond_1(element) and self._cond_2(element)