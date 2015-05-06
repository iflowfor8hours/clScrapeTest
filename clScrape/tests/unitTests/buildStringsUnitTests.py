import unittest
from clScrape.buildStrings import getStrings, getMake, getModel, getYears, getPrice, getKeyWords

class TestCase(unittest.TestCase):
  global goodVals, baseString
  goodVals = {'site':'testSite',
              'Ford':'make',
              'F150':'model',
              'minYear':'2004',
              'maxYear':'2005',
              'minPrice':'1',
              'maxPrice':'5000',
              'needs':'keywords',
              '5.4':'keywords'
             }
  baseString = 'http://testSite.craigslist.org/search/sso?'
  def setUp(self):
    pass
  
  def tearDown(self):
    pass
    
  def testGetStrings(self):
    results = getStrings(goodVals)
    string0 = baseString + 'autoMakeModel=Ford+F150&autoMinYear=2004&autoMaxYear=2005&minAsk=1&maxAsk=5000&query="needs"'
    string1 = baseString + 'autoMakeModel=Ford+F150&autoMinYear=2004&autoMaxYear=2005&minAsk=1&maxAsk=5000&query="5.4"'
    self.assertEqual(results[0]['querySet'],'needs','Invalid querySet for results[0]')
    self.assertEqual(results[1]['querySet'],'5.4','Invalid querySet for results[1]')
    self.assertEqual(results[0]['string'],string0,'Invalid url string for full results[0]')
    self.assertEqual(results[1]['string'],string1,'Invalid url string for full results[1]')
  
  def testGetMake(self):
    results = getMake([baseString],{})
    string0 = baseString 
    self.assertEqual(results[0],string0,'Invalid url string for make results[0] string 0')
    
    results = getMake([baseString],{'Ford':goodVals['Ford']})
    string1 = baseString + 'autoMakeModel=Ford'
    self.assertEqual(results[0],string1,'Invalid url string for make results[0] string 1')
        
  def testGetModel(self):
    baseStringPlusModel = baseString + 'autoMakeModel=Ford' 
    results = getModel([baseString,baseStringPlusModel],{})
    string0 = baseString 
    self.assertEqual(results[0],string0,'Invalid url string for model results[0] string 0')
    self.assertEqual(results[1],baseStringPlusModel,'Invalid url string for model results[1] string bspm')
    
    results = getModel([baseStringPlusModel, baseString] , {'F150':goodVals['F150']} )
    string1 = baseString + 'autoMakeModel=F150'
    string2 = baseString + 'autoMakeModel=Ford+F150'
    self.assertEqual(results[0],string2,'Invalid url string for make results[0] string 2')
    self.assertEqual(results[1],string1,'Invalid url string for make results[1] string 1')
        
  def testGetYears(self):
    baseStringPlusModel = baseString + 'autoMakeModel=Ford' 
    results = getYears([baseString,baseStringPlusModel],{})
    string0 = baseString 
    self.assertEqual(results[0],string0,'Invalid url string for year results[0] string 0')
    self.assertEqual(results[1],baseStringPlusModel,'Invalid url string for model results[1] string bspm')
    
    results = getYears([baseStringPlusModel, baseString] , {'minYear':goodVals['minYear']} )
    string1 = baseString + '&autoMinYear=2004'
    string2 = baseString + 'autoMakeModel=Ford&autoMinYear=2004'
    self.assertEqual(results[0],string2,'Invalid url string for minYear results[0] string 2')
    self.assertEqual(results[1],string1,'Invalid url string for minYear results[1] string 1')
    
    results = getYears([baseStringPlusModel, baseString] , {'maxYear':goodVals['maxYear']} )
    string3 = baseString + '&autoMaxYear=2005'
    string4 = baseString + 'autoMakeModel=Ford&autoMaxYear=2005'
    self.assertEqual(results[0],string4,'Invalid url string for minYear results[0] string 4')
    self.assertEqual(results[1],string3,'Invalid url string for maxYear results[1] string 3')
    
    results = getYears([baseStringPlusModel, baseString] , {'minYear':goodVals['minYear'],'maxYear':goodVals['maxYear']})
    string5 = baseString + '&autoMinYear=2004&autoMaxYear=2005'
    string6 = baseString + 'autoMakeModel=Ford&autoMinYear=2004&autoMaxYear=2005'
    self.assertEqual(results[0],string6,'Invalid url string for make results[0] string 2')
    self.assertEqual(results[1],string5,'Invalid url string for make results[1] string 1')
    
    badMin = [{'minYear':'200','maxYear':'2005'},
               {'minYear':'200a','maxYear':'2005'},
               {'minYear':'-2000','maxYear':'2005'},
               {'minYear':'#$%^','maxYear':'2005'},
             ]
    badMax = [{'minYear':'2004','maxYear':'200'},
               {'minYear':'2004','maxYear':'200a'},
               {'minYear':'2004','maxYear':'-2005'},
               {'minYear':'2004','maxYear':'*&^%'}
              ]
    for bn in badMin:
      results = getYears([baseString] , bn)
      self.assertNotIn('MinYear',results[0],'Bad Min Year Entry did not fail:' + str(bn))
    
    for bx in badMax:
      results = getYears([baseString] , bx)
      self.assertNotIn('MaxYear',results[0],'Bad Max Year Entry did not fail:' + str(bn))
    
  def testGetPrice(self):
    assert 1 == 1
    
  def testGetKeywords(self):
    assert 1 == 1

if __name__ == '__main__':
    unittest.main()