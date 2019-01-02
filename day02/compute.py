"""
Answer to https://adventofcode.com/2018/day/2
"""
from collections import defaultdict
from typing import List


class ID(object):

    def __init__(self, word: str):
        self.word = word
        _letter_freq = defaultdict(lambda: 0)

        for l in word:
            _letter_freq[l] += 1

        self.reversed_letter_freq = defaultdict(lambda: 0)
        for c in _letter_freq.values():
            self.reversed_letter_freq[c] += 1

    @classmethod
    def from_file(cls, filename: str):  # -> List[str, ID]:
        elements = []
        with open(filename) as f:
            for l in f.readlines():
                elements.append(cls(l.rstrip()))

        print('Loaded %d elements from %s' % (len(elements), filename))
        return elements

    @classmethod
    def checksum(cls, elements: List):
        rv = defaultdict(lambda: 0)
        for _id in elements:
            for k, v in _id.reversed_letter_freq.items():
                rv[k] += 1
        return rv[2] * rv[3]

    @classmethod
    def compare(cls, elements: List):
        # returns the common letters
        for i, _id in enumerate(elements):
            for other in elements[i:]:
                common = _id.common(other)
                num_diff = len(other.word) - len(common)
                # print('%d differences between %s and %s.' % (num_diff, _id.word, other.word))
                if 1 == num_diff:
                    return common

    def common(self, other):
        _common = ''
        # assumes len(other.word) == len(self.word)
        assert len(other.word) == len(self.word), '%r vs %r' % (other.word, self.word)
        for i, l in enumerate(self.word):
            if l == other.word[i]:
                _common += l
        return _common


if '__main__' == __name__:

    inventory = ID.from_file('input.txt')

    checksum = ID.checksum(inventory)
    print('Checksum is %d' % checksum)  # 3952

    similar_words = ID.compare(inventory)
    print('Common letters are %s' % similar_words)  # vtnikorkulbfejvyznqgdxpaw
