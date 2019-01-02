from day5.compute import reaction, simplification


def test_reaction():
    expected = 'dabCBAcaDA'

    for input in ('dabCBAcaDA', 'dabCBAcCcaDA', 'dabAaCBAcCcaDA', 'dabAcCaCBAcCcaDA'):
        rv = reaction(input).polymere
        assert expected == rv, 'got %s' % rv

    rv = reaction('PpVviIcPpaACHKkhcvNnVhXxtTsSTtbBHUvmMVuUAakKhHyQqYuay').polymere
    assert 'cay' == rv, 'got %s' % rv


def test_simplification():
    rv = simplification('dabAcCaCBAcCcaDA', 'a')
    assert 'dbcCCBcCcD' == rv, 'got %s' % rv
    rv = simplification('dabAcCaCBAcCcaDA', 'B')
    assert 'daAcCaCAcCcaDA' == rv, 'got %s' % rv
    rv = simplification('dabAcCaCBAcCcaDA', 'c')
    assert 'dabAaBAaDA' == rv, 'got %s' % rv
    rv = simplification('dabAcCaCBAcCcaDA', 'd')
    assert 'abAcCaCBAcCcaA' == rv, 'got %s' % rv
