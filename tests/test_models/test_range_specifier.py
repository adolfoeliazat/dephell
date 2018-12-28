# external
import pytest

# project
from dephell.models.range_specifier import RangeSpecifier


@pytest.mark.parametrize('operator, mask', [
    ('<',   [1, 0, 0]),
    ('<=',  [1, 1, 0]),
    ('==',  [0, 1, 0]),
    ('===', [0, 1, 0]),
    ('>=',  [0, 1, 1]),
    ('>',   [0, 0, 1]),
])
def test_simple(operator, mask):
    versions = ('1.2.3', '1.3.2', '1.4.1')
    spec = RangeSpecifier(operator + '1.3.2')
    for version, ok in zip(versions, mask):
        assert (version in spec) == ok


@pytest.mark.parametrize('op1, op2, mask', [
    # left
    ('<',   '<',    [1, 0, 0, 0, 0]),
    ('<',   '<=',   [1, 0, 0, 0, 0]),
    ('<=',  '<',    [1, 1, 0, 0, 0]),
    ('<=',  '<=',   [1, 1, 0, 0, 0]),
    ('==',  '<',    [0, 1, 0, 0, 0]),
    ('==',  '<=',   [0, 1, 0, 0, 0]),

    # center
    ('>=',  '<',    [0, 1, 1, 0, 0]),
    ('>',   '<',    [0, 0, 1, 0, 0]),
    ('>',   '<=',   [0, 0, 1, 1, 0]),
    ('>=',  '<=',   [0, 1, 1, 1, 0]),

    # right
    ('>=',  '==',   [0, 0, 0, 1, 0]),
    ('>',   '==',   [0, 0, 0, 1, 0]),
    ('>',   '>=',   [0, 0, 0, 1, 1]),
    ('>=',  '>=',   [0, 0, 0, 1, 1]),
    ('>=',  '>',    [0, 0, 0, 0, 1]),
    ('>',   '>',    [0, 0, 0, 0, 1]),

    # incompat
    ('<=',  '>=',   [0, 0, 0, 0, 0]),
    ('<',   '>=',   [0, 0, 0, 0, 0]),
    ('<=',  '>',    [0, 0, 0, 0, 0]),
    ('<',   '>',    [0, 0, 0, 0, 0]),
    ('==',  '==',   [0, 0, 0, 0, 0]),
    ('==',  '>',    [0, 0, 0, 0, 0]),
    ('==',  '>=',   [0, 0, 0, 0, 0]),
    ('<',   '==',   [0, 0, 0, 0, 0]),
    ('<=',  '==',   [0, 0, 0, 0, 0]),
])
def test_range(op1, op2, mask):
    versions = ('1.2.3', '1.3.2', '1.4.1', '1.5.1', '1.6.1')
    spec = RangeSpecifier(op1 + '1.3.2,' + op2 + '1.5.1')
    for version, ok in zip(versions, mask):
        assert (version in spec) == ok


# ^1.2.3 := >=1.2.3 <2.0.0
@pytest.mark.parametrize('specv, version, ok', [
    ('1.2.3', '1.2.3', True),
    ('1.2.3', '1.2.4', True),
    ('1.2.3', '1.3.1', True),
    ('1.2.3', '1.3.0', True),

    ('1.2.3', '1.2.2', False),
    ('1.2.3', '1.1.9', False),
    ('1.2.3', '1.0.0', False),
    ('1.2.3', '2.0.0', False),
    ('1.2.3', '3.0.0', False),

    ('1.2.0', '1.2.0', True),
    ('1.2.0', '1.2.1', True),
    ('1.2.0', '1.3.2', True),

    ('1.2.0', '1.1.0', False),
    ('1.2.0', '0.9.0', False),
    ('1.2.0', '2.0.0', False),

    ('1.0.0', '1.0.0', True),
    ('1.0.0', '1.0.1', True),
    ('1.0.0', '1.1.0', True),
    ('1.0.0', '2.0.0', False),
    ('1.0.0', '0.9.0', False),

    ('1.0',   '1.0.0', True),
    ('1.0',   '1.0.1', True),
    ('1.0',   '1.1.0', True),
    ('1.0',   '2.0.0', False),
    ('1.0',   '0.9.0', False),

    ('1',     '1.0.0', True),
    ('1',     '1.0.1', True),
    ('1',     '1.1.0', True),
    ('1',     '2.0.0', False),
    ('1',     '0.9.0', False),
])
def test_caret(specv, version, ok):
    spec = RangeSpecifier('^' + specv)
    assert (version in spec) is ok


# ~1.2.3 := >=1.2.3 <1.3.0
@pytest.mark.parametrize('specv, version, ok', [
    ('1.2.3', '1.2.3', True),
    ('1.2.3', '1.2.4', True),

    ('1.2.3', '1.3.1', False),
    ('1.2.3', '1.3.0', False),
    ('1.2.3', '1.2.2', False),
    ('1.2.3', '1.1.9', False),
    ('1.2.3', '1.0.0', False),
    ('1.2.3', '2.0.0', False),
    ('1.2.3', '3.0.0', False),

    ('1.2.0', '1.2.0', True),
    ('1.2.0', '1.2.1', True),

    ('1.2.0', '1.3.2', False),
    ('1.2.0', '1.1.0', False),
    ('1.2.0', '0.9.0', False),
    ('1.2.0', '2.0.0', False),

    ('1.0.0', '1.0.0', True),
    ('1.0.0', '1.0.1', True),
    ('1.0.0', '1.1.0', False),
    ('1.0.0', '2.0.0', False),
    ('1.0.0', '0.9.0', False),

    ('1.0',   '1.0.0', True),
    ('1.0',   '1.0.1', True),
    ('1.0',   '1.1.0', False),
    ('1.0',   '2.0.0', False),
    ('1.0',   '0.9.0', False),

    ('1',     '1.0.0', True),
    ('1',     '1.0.1', True),
    ('1',     '1.1.0', False),
    ('1',     '2.0.0', False),
    ('1',     '0.9.0', False),
])
def test_tilda(specv, version, ok):
    spec = RangeSpecifier('~' + specv)
    assert (version in spec) is ok


@pytest.mark.parametrize('version, ok', [
    ('2.7',     True),
    ('2.7.1',   True),
    ('2.7.6',   True),

    ('2.8',     False),
    ('2.8.0',   False),
    ('3.0',     False),

    ('3.2',     True),
    ('3.2.1',   True),
    ('3.3',     True),
    ('3.7',     True),

    ('4.0',     False),
])
def test_or(version, ok):
    spec = RangeSpecifier('~2.7 || ^3.2')
    assert (version in spec) is ok