import unittest
from clScrape.__init__ import setFunction, getValues

class TestCase(unittest.TestCase):
  def setUp(self):
    pass
  
  def tearDown(self):
    pass
  
  def testSetFunction(self):
    assert 1 == 1
  
  def testGetValues(self):
    assert 1 == 1

if __name__ == '__main__':
    unittest.main()