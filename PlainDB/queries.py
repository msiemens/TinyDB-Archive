__all__ = 'has'


class query(object):
    """
    The baisc query used for integer like comparisons (==, >, <, ...)
    """

    def __init__(self, key):
        self._key = key
        self._repr = '<has>'

    def __eq__(self, other):
        """
        Equals el[key] == other
        """
        self._value_eq = other
        self._update_repr('==', other)
        return self

    def __lt__(self, other):
        """
        Equals el[key] < other
        """
        self._value_lt = other
        self._update_repr('<', other)
        return self

    def __le__(self, other):
        """
        Equals el[key] <= other
        """
        self._value_le = other
        self._update_repr('<=', other)
        return self

    def __gt__(self, other):
        """
        Equals el[key] > other
        """
        self._value_gt = other
        self._update_repr('>', other)
        return self

    def __ge__(self, other):
        """
        Equals el[key] >= other
        """
        self._value_ge = other
        self._update_repr('>=', other)
        return self

    def __or__(self, other):
        """
        Equals self | other
        See :class:`query_or`.
        """
        return query_or(self, other)

    def __and__(self, other):
        """
        Equals self & other
        See :class:`query_and`.
        """
        return query_and(self, other)

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

        return True  # _key exists in element (see above)

    def _update_repr(self, operator, value):
        self._repr = '\'{}\' {} {}'.format(self._key, operator, value)

    def __repr__(self):
        return self._repr

has = query


class query_or(object):
    """
    Combines to queries with a logical 'or'.
    """
    def __init__(self, where1, where2):
        self._cond_1 = where1
        self._cond_2 = where2

    def __and__(self, other):
        return query_and(self, other)

    def __or__(self, other):
        return query_or(self, other)

    def __call__(self, element):
        return self._cond_1(element) or self._cond_2(element)

    def __repr__(self):
        return '({}) or ({})'.format(self._cond_1, self._cond_2)


class query_and(object):
    """
    Combines to queries with a logical 'and'.
    """
    def __init__(self, where1, where2):
        self._cond_1 = where1
        self._cond_2 = where2

    def __and__(self, other):
        return query_and(self, other)

    def __or__(self, other):
        return query_or(self, other)

    def __call__(self, element):
        return self._cond_1(element) and self._cond_2(element)

    def __repr__(self):
        return '({}) and ({})'.format(self._cond_1, self._cond_2)