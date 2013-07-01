import os
import tempfile
import string
import random
random.seed()

from PlainDB.backends import YAMLBackend
from nose.tools import *

path = None
element = None
element = {
    'type': 'string',
    'length': 5,
    'chars': [
        'a', 'b', 'c', 'd', 'e'
    ],
    'ready': True
}


def setup():
    global path, element

    # Generate temp file
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.file.close()  # Close file handle
    path = tmp.name


def teardown():
    # Cleanup
    os.unlink(path)


def test_yaml():
    # Write contents
    backend = YAMLBackend(path)
    backend.write(element)

    # Verify contents
    assert_equal(element, backend.read())
