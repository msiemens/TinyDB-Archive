from abc import ABCMeta, abstractmethod

import yaml


class Backend(ABCMeta, object):
    """
    A generic backend to PlainDB.
    """

    @abstractmethod
    def __init__(self, path):
        raise NotImplementedError('To be overriden!')

    @abstractmethod
    def write(self, data):
        raise NotImplementedError('To be overriden!')

    @abstractmethod
    def read(self):
        raise NotImplementedError('To be overriden!')


class YAMLBackend(Backend):
    """
    Store the data in a YAML file.
    """

    def __init__(self, path):
        self._handle = open(path, 'r+')

    def write(self, data):
        self._handle.seek(0)
        yaml.dump(data)

    def read(self):
        return yaml.load(self._handle)