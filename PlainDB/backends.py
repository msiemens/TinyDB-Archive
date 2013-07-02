from abc import ABCMeta, abstractmethod

import os

import yaml


def touch(fname, times=None):
    with file(fname, 'a'):
        os.utime(fname, times)


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
    # TODO: Add caching

    def __init__(self, path):
        super(YAMLBackend, self).__init__()
        touch(path)  # Create file if not exists
        self._handle = open(path, 'r+')

    def write(self, data):
        self._handle.seek(0)
        yaml.dump(data, self._handle)
        self._handle.flush()

    def read(self):
        self._handle.seek(0)
        return yaml.load(self._handle)


class MemoryBackend(Backend):
    """
    Store the data as YAML in memory.
    """

    def __init__(self, path=None):
        super(MemoryBackend, self).__init__()
        self.memory = ''

    def write(self, data):
        self.memory = yaml.dump(data)

    def read(self):
        return yaml.load(self.memory)
