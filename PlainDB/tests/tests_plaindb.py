from PlainDB import PlainDB, has
from PlainDB.backends import MemoryBackend

from nose.tools import *

#: :type: PlainDB
db = None

def setup():
    global db
    db = PlainDB('<memory>', backend=MemoryBackend)


def test_purge():
    db.insert({})
    db.purge()

    assert_equal(len(db), 0)


def test_all():
    db.purge()

    for i in range(10):
        db.insert({})

    assert_equal(len(db), 10)


def test_insert():
    db.purge()

    db.insert({'int': 1, 'char': 'a'})
    assert_equal(len(db.search(has('int') == 1)), 1)


def test_insert_multiple():
    db.purge()

    db.insert({'int': 1, 'char': 'a'})
    db.insert({'int': 1, 'char': 'b'})
    db.insert({'int': 1, 'char': 'c'})

    assert_equal(len(db.search(has('int') == 1)), 3)
    assert_equal(len(db.search(has('char') == 'a')), 1)


def test_remove():
    db.purge()

    db.insert({'int': 1, 'char': 'a'})
    db.insert({'int': 1, 'char': 'b'})
    db.insert({'int': 1, 'char': 'c'})

    db.remove(has('char') == 'b')

    assert_equal(len(db), 2)


def test_search():
    db.purge()

    db.insert({'int': 1, 'char': 'a'})
    db.insert({'int': 1, 'char': 'b'})
    db.insert({'int': 1, 'char': 'c'})

    results = db.search(has('int') == 1)
    assert_equal(len(results), 3)

    assert_equal(results[0]['char'], 'a')
    assert_equal(results[1]['char'], 'b')
    assert_equal(results[2]['char'], 'c')

def test_get():
    db.purge()

    db.insert({'int': 1, 'char': 'a'})
    db.insert({'int': 1, 'char': 'b'})
    db.insert({'int': 1, 'char': 'c'})

    assert_equal(db.get(has('int') == 1)['char'], 'a')
    assert_equal(db.get(has('char') == 'b')['char'], 'b')