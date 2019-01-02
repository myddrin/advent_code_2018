"""
Answer to https://adventofcode.com/2018/day/1
"""
with open('input.txt') as f:
    changes = [int(l) for l in f.readlines()]

freq = 0
freq_history = set()
final_freq = None
loops = 0

while final_freq is None:
    for l in changes:
        freq += l
        if freq in freq_history:
            final_freq = freq
            break
        freq_history.add(freq)
    if 0 == loops:
        print('Stabilised at freq %d' % freq)
    #if 0 == loops%1000000:
    #	print('loops=%d freq=%d history_len=%d' % (loops, freq, len(freq_history)))
    loops += 1

print('First duplicate freq %d (in %d loops)' % (final_freq, loops))