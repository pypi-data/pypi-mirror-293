import compressbins.compressbins as cb
import pytest
import numpy as np

def test_compress_bins():
    assert cb.compress_bins([0,2,4,6,8,10]) == ['0-2','2-4','4-6','6-8','8-10']

def test_compress_bins_floats():
    assert cb.compress_bins([0.0,2.0,4.0,6.0,8.0,10.0]) == ['0.0-2.0','2.0-4.0','4.0-6.0','6.0-8.0','8.0-10.0']

def test_short_floats():
    assert cb.compress_bins([0.0,2.0,3.0]) == ['0.0-2.0','2.0-3.0']

def test_shortest_valid_floats():
    assert cb.compress_bins([0.0,2.0]) == ['0.0-2.0']

def test_list_of_strings():
    assert cb.compress_bins(['0.0','2.2']) == ['0.0-2.2']

def test_list_numpy_floats():
    array = np.array([0.0,2.2], dtype=np.float64)
    print(array)
    assert cb.compress_bins([0.0,2.2]) == ['0.0-2.2']


def test_empty_floats():
    try:
        cb.compress_bins([])
    except ValueError as e:
        assert str(e) == 'bins must be an array of length >= 2'
        return
    pytest.fail()

def test_not_list():
    try:
        cb.compress_bins(2.2)
    except ValueError as e:
        assert str(e) == 'bins must be an array of length >= 2'
        return
    pytest.fail()
