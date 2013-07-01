from abc import ABCMeta, abstractmethod

import yaml


class Backend(object):
    """
    A generic backend to PlainDB.
    """
    __metaclass__ = ABCMeta

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
        super(YAMLBackend, self).__init__()
        self._handle = open(path, 'r+')

    def write(self, data):
        self._handle.seek(0)
        yaml.dump(data, self._handle)
        self._handle.flush()

    def read(self):
        self._handle.seek(0)
        return yaml.load(self._handle)