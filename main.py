import numpy
import hashlib
import logging
import math

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class BloomFilter:

    def __init__(self, bits, rounds):
        self.bits = bits
        self.bytes = int(bits / 8)
        if self.bytes * 8 != self.bits:
            raise ValueError('Need byte boundary bit value')
        self.rounds = rounds
        self.filter = numpy.zeros(self.bytes, dtype=numpy.uint8)


    def add(self, s):
        for i in range(self.rounds):
            salt = str(i)
            salt_str = salt.encode('utf-8')
            logg.debug('hashing {} {}'.format(s, salt))
            h = hashlib.sha256()
            h.update(s.encode('utf-8'))
            h.update(salt_str)
            z = h.digest()
            r = int.from_bytes(z, byteorder='big')
            m = r % self.bits
            bytepos = math.floor(m / 8)
            bitpos = m % 8
            self.filter[bytepos] |= 1 << bitpos
            logg.debug('foo {} {}'.format(bytepos, bitpos))
        return m


f = BloomFilter(8192 * 8, 3)
f.add('1024')
