import re

__all__ = 'has'


class AndOrMixin(object):
    """
    TODO: Docstring
    """
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


class query(AndOrMixin):
    """
    The baisc query used for integer like comparisons (==, >, <, ...)
    """

    def __init__(self, key):
        self._key = key
        self._repr = '<has>'

    def matches(self, regex):
        """
        Equals self.matches(...).
        """
        return query_regex(self._key, regex)

    def __eq__(self, other):
        """
        Equals el[key] == other
        """
        self._value_eq = other
        self._update_repr('==', other)
        return self

    def __ne__(self, other):
        """
        Equals ! self
        See :class:`query_not`.
        """
        self._value_ne = other
        self._update_repr('!=', other)
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

    def __invert__(self):
        """
        Equals ~ self
        See :class:`query_not`.
        """
        return query_not(self)

    def __call__(self, element):
        if self._key not in element:
            return False

        try:
            return element[self._key] == self._value_eq
        except AttributeError:
            pass

        try:
            return element[self._key] != self._value_ne
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


class query_not(AndOrMixin):
    """
    Negates a query
    """
    def __init__(self, cond):
        self._cond = cond

    def __call__(self, element):
        return not self._cond(element)

    def __repr__(self):
        return 'not ({})'.format(self._cond)


class query_or(AndOrMixin):
    """
    Combines to queries with a logical 'or'.
    """
    def __init__(self, where1, where2):
        self._cond_1 = where1
        self._cond_2 = where2

    def __call__(self, element):
        return self._cond_1(element) or self._cond_2(element)

    def __repr__(self):
        return '({}) or ({})'.format(self._cond_1, self._cond_2)


class query_and(AndOrMixin):
    """
    Combines to queries with a logical 'and'.
    """
    def __init__(self, where1, where2):
        self._cond_1 = where1
        self._cond_2 = where2

    def __call__(self, element):
        return self._cond_1(element) and self._cond_2(element)

    def __repr__(self):
        return '({}) and ({})'.format(self._cond_1, self._cond_2)


class query_regex(AndOrMixin):
    """
    Lets check a field value against a regex.
    """
    def __init__(self, key, regex):
        self.regex = regex
        self._key = key

    def __call__(self, element):
        return bool(self._key in element
                and re.match(self.regex, element[self._key]))

    def __repr__(self):
        return '\'{}\' ~= {} '.format(self._key, self.regex)