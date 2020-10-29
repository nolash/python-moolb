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
        self.hasher = self.__hash


    def add(self, b):
        for i in range(self.rounds):
            salt = str(i)
            s = salt.encode('utf-8')
            z = self.__hash(b, s)
            r = int.from_bytes(z, byteorder='big')
            m = r % self.bits
            bytepos = math.floor(m / 8)
            bitpos = m % 8
            self.filter[bytepos] |= 1 << bitpos
            logg.debug('foo {} {}'.format(bytepos, bitpos))
        return m


    def check(self, b):
        for i in range(self.rounds):
            salt = str(i)
            s = salt.encode('utf-8')
            z = self.__hash(b, s)
            r = int.from_bytes(z, byteorder='big')
            m = r % self.bits
            bytepos = math.floor(m / 8)
            bitpos = m % 8
            if not self.filter[bytepos] & 1 << bitpos:
                return False
            return True


    def __hash(self, b, s):
       logg.debug('hashing {} {}'.format(b.hex(), s.hex()))
       h = hashlib.sha256()
       h.update(b)
       h.update(s)
       return h.digest()



f = BloomFilter(8192 * 8, 3)
f.add(b'1024')
print(f.check(b'1024'))
print(f.check(b'1023'))
