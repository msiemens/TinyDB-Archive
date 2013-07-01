import yaml


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


class PlainDB(object):
    """
    A simple DB storing all types of python objects using a YAML file.
    """

    def __init__(self, path):
        self._handle = open(path, 'r+')
        try:
            self._last_id = self._read_yaml().pop()['id']
        except IndexError:
            self._last_id = 0

    def _read_yaml(self):
        """
        Reading access to the yaml backend.

        :returns: all values
        :rtype: list
        """

        self._handle.seek(0)  # Move file pointer to file begin
        values = yaml.load(self._handle)
        return values or []

    def _write_yaml(self, values):
        """
        Writing access to the yaml backend

        :param values: the new values to write
        :type values: list
        """

        self._handle.seek(0)
        yaml.dump(values, self._handle)
        self._handle.flush()

    def all(self):
        """
        Get all elements stored in the DB.

        :returns: a list of al elements.
        :rtype: list
        """

        return self._read_yaml()

    def insert(self, element):
        """
        Insert a new element into the db.

        element has to be a dict, not containing the key 'id'.
        """

        self._last_id += 1
        element['id'] = self._last_id

        values = self._read_yaml()
        values.append(element)

        self._write_yaml(values)

    def remove(self, where):
        """
        Remove the element matching the condition.

        :param where: the condition
        :type where: has
        """

        to_remove = self.search(where)
        self._write_yaml([e for e in self._read_yaml() if e != to_remove])

    def search(self, where):
        """
        Search for all elements matching a 'where' condition.

        :param where: the condition
        :type where: has

        :returns: list of matching elements
        :rtype: list
        """

        return [e for e in self._read_yaml() if where(e)]

    def get(self, where):
        """
        Search for exactly one element matching a 'where' condition.

        :param where: the condition
        :type where: has

        :returns: the element or None
        :rtype: dict or None
        """

        for el in self._read_yaml():
            if where(el):
                return el