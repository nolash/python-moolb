import unittest
import hashlib

from moolb import Bloom


def hashround(self, b, s):
       logg.debug('sha1 hashing {} {}'.format(b.hex(), s.hex()))
       h = hashlib.sha1()
       h.update(b)
       h.update(s)
       return h.digest()


class Test(unittest.TestCase):

    def test_default(self):
        f = Bloom(8192 * 8, 3)
        f.add(b'1024')
        self.assertTrue(f.check(b'1024'))
        self.assertFalse(f.check(b'1023'))

    
    def test_plug(self):
        f = Bloom(8192 * 8, 3, hashround)
        f.add(b'1024')
        self.assertTrue(f.check(b'1024'))
        self.assertFalse(f.check(b'1023'))


if __name__ == '__main__':
    unittest.main()
