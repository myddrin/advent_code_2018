from day2.compute import ID


def test_1():
    inventory = ID.from_file('test1.txt')
    checksum = ID.checksum(inventory)

    assert 12 == checksum


def test_2():
    inventory = ID.from_file('test2.txt')
    checksum = ID.checksum(inventory)

    common = ID.compare(inventory)
    print('common=%r' % common)
    assert 'fgij' == common
