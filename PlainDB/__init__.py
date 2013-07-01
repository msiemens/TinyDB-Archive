from PlainDB.queries import has

from backends import Backend, YAMLBackend


class PlainDB(object):
    """
    A simple DB storing all types of python objects using a YAML file.
    """

    def __init__(self, path, backend=YAMLBackend):
        #: :type: Backend
        self._backend = backend(path)

        try:
            self._last_id = self._read().pop()['id']
        except IndexError:
            self._last_id = 0

    def _read(self):
        """
        Reading access to the backend.

        :returns: all values
        :rtype: list
        """

        return self._backend.read() or []

    def _write(self, values):
        """
        Writing access to the backend

        :param values: the new values to write
        :type values: list
        """

        self._backend.write(values)

    def __len__(self):
        return len(self.all())

    def all(self):
        """
        Get all elements stored in the DB.

        :returns: a list of al elements.
        :rtype: list
        """

        return self._read()

    def insert(self, element):
        """
        Insert a new element into the db.

        element has to be a dict, not containing the key 'id'.
        """

        self._last_id += 1
        element['id'] = self._last_id

        values = self._read()
        values.append(element)

        self._write(values)

    def remove(self, where):
        """
        Remove the element matching the condition.

        :param where: the condition
        :type where: has
        """

        to_remove = self.get(where)
        self._write([e for e in self._read() if e != to_remove])

    def purge(self):
        """
        Purge the DB by removing all elements.
        """
        self._write([])

    def search(self, where):
        """
        Search for all elements matching a 'where' condition.

        :param where: the condition
        :type where: has

        :returns: list of matching elements
        :rtype: list
        """

        return [e for e in self._read() if where(e)]

    def get(self, where):
        """
        Search for exactly one element matching a 'where' condition.

        :param where: the condition
        :type where: has

        :returns: the element or None
        :rtype: dict or None
        """

        for el in self._read():
            if where(el):
                return el