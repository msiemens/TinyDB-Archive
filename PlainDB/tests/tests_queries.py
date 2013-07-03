from nose.tools import *

from PlainDB.queries import has


def test_eq():
    query = has('value') == 1
    assert_true(query({'value': 1}))
    assert_false(query({'value': 2}))


def test_ne():
    query = has('value') != 1
    assert_true(query({'value': 2}))
    assert_false(query({'value': 1}))


def test_lt():
    query = has('value') < 1
    assert_true(query({'value': 0}))
    assert_false(query({'value': 1}))


def test_le():
    query = has('value') <= 1
    assert_true(query({'value': 0}))
    assert_true(query({'value': 1}))
    assert_false(query({'value': 2}))

def test_gt():
    query = has('value') > 1
    assert_true(query({'value': 2}))
    assert_false(query({'value': 1}))


def test_ge():
    query = has('value') >= 1
    assert_true(query({'value': 2}))
    assert_true(query({'value': 1}))
    assert_false(query({'value': 0}))


def test_or():
    query = (
        (has('val1') == 1) |
        (has('val2') == 2)
    )
    assert_true(query({'val1': 1}))
    assert_true(query({'val2': 2}))
    assert_true(query({'val1': 1, 'val2': 2}))
    assert_false(query({'val1': '', 'val2': ''}))


def test_and():
    query = (
        (has('val1') == 1) &
        (has('val2') == 2)
    )
    assert_true(query({'val1': 1, 'val2': 2}))
    assert_false(query({'val1': 1}))
    assert_false(query({'val2': 2}))
    assert_false(query({'val1': '', 'val2': ''}))


def test_not():
    query = ~ (has('val1') == 1)
    assert_true(query({'val1': 5, 'val2': 2}))
    assert_false(query({'val1': 1, 'val2': 2}))

    query = (
        (~ (has('val1') == 1)) &
        (has('val2') == 2)
    )
    assert_true(query({'val1': '', 'val2': 2}))
    assert_true(query({'val2': 2}))
    assert_false(query({'val1': 1, 'val2': 2}))
    assert_false(query({'val1': 1}))
    assert_false(query({'val1': '', 'val2': ''}))


def test_has_key():
    query = has('val3')

    assert_true(query({'val3': 1}))
    assert_false(query({'val1': 1, 'val2': 2}))
