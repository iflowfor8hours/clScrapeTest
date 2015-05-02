import unittest
import buildStringsUnitTests
import getRangeSitesUnitTests
import getRequestResultsUnitTests
import getValuesUnitTests
import initUnitTests
import parseHTMLunitTests
import updateCLzipsUnitTests

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(buildStringsUnitTests.TestCase))
  suite.addTest(unittest.makeSuite(getRangeSitesUnitTests.TestCase))
  suite.addTest(unittest.makeSuite(getRequestResultsUnitTests.TestCase))
  suite.addTest(unittest.makeSuite(getValuesUnitTests.TestCase))
  suite.addTest(unittest.makeSuite(initUnitTests.TestCase))
  suite.addTest(unittest.makeSuite(parseHTMLunitTests.TestCase))
  suite.addTest(unittest.makeSuite(updateCLzipsUnitTests.TestCase))
  return suite

if __name__ == '__main__':
  runner = unittest.TextTestRunner()
  test_suite = suite()
  runner.run (test_suite)
    
