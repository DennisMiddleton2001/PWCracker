#!/usr/bin/python3
import sspilib
import unittest
import md4
import binascii

class TestProvidedVectors(unittest.TestCase):
    s = sspilib.UserCredential("dave", 'password')
    def test_equals_expected(self):
      for (msg, digest) in md4.md4_test:
        m = md4.MD4()
        m.update(msg.encode('us-ascii'))
        d = m.digest()
        print(d)

        self.assertEqual(binascii.hexlify(d).decode('us-ascii'), '%032x' % digest)

if __name__ == '__main__':
    unittest.main()
