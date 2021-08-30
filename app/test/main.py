import os
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest

from extract.extractor import extract, Extractor

def add(x,y):
    return x + y

class MyTest(unittest.TestCase):
    def setUp(self):
        self.lst = ['1','2','4']

    def testHello(self):
        b = Extractor('>bbbbbb')
        self.assertEqual(b.hello(), '>bbbbbb')

if __name__ == '__main__':
    unittest.main()
