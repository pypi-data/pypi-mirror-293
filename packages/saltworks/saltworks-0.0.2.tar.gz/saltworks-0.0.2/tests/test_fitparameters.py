import numpy as np
import pytest

from saltworks.fitparameters import FitParameters, Structure, structarray


def test_structure():
    s = Structure([('a', 7), 3])
    assert 10 == len(s)
    assert ['a', '__0__'] == [str(name) for name in s]
    assert 4 == len(Structure([('a', 3), 'b']))


def test_structarray():
    v = structarray(np.zeros(10), [('a', 3), ('b', 7)])
    assert np.allclose(np.asarray([ 0.,  0.,  0.]), v['a'])

    C = structarray(np.zeros((10,10)), [('a', 2), ('b', 8)])
    assert np.allclose(np.asarray([[0, 0], [0, 0]]), C['a', 'a'])


@pytest.fixture
def params():
    return FitParameters([('alpha', 2), ('S', 3), ('dSdT', 2), 'idark'])


def test_fitparameters_set(params):
    params['idark'][0] = -1
    params['idark'] = -2.1548
    params['S'][1] = 4
    params['dSdT'][:] = 42.

    assert len(params.full) == 8
    assert len(params.free) == 8
    assert np.allclose(
        np.asarray([0., 0., 0., 4., 0., 42., 42., -2.1548]),
        np.asarray(params.full))


def test_fitparameters_fix(params):
    params.fix(0, 30)
    params.fix(-2, 2)

    assert len(params.full) == 8
    assert len(params.free) == 6
    assert np.allclose(
        np.asarray([30., 0., 0., 0., 0., 0., 2, 0.]),
        np.asarray(params.full))


def test_fitparameters_fix_named(params):
    params['S'].fix([1, -1], 30)
    params['alpha'].fix(val=1e-3)
    params['dSdT'].fix()

    assert len(params.full) == 8
    assert len(params.free) == 2
    assert np.allclose(
        np.asarray([1e-3, 1e-3, 0., 30, 30, 0, 0, 0]),
        np.asarray(params.full))
    assert np.allclose(
        np.asarray([0., 0]),
        np.asarray(params.free))


def test_fitparameters_free(params):
    params.free[0] = 12
    assert params.free[0] == 0

    params['S'].free = 5
    assert np.allclose(
        np.asarray([0., 0., 5., 5., 5., 0., 0., 0.]),
        np.asarray(params.full))


def test_fitparameter_indexof(params):
    assert list(params['dSdT'].indexof()) == [5, 6]
    params['dSdT'].fix(1)
    assert list(params['dSdT'].indexof()) == [5, -1]
