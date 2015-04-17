
from urllib2 import Request, urlopen, URLError

def getRequestResults(site):
  request = Request(site)
  try :
    response = urlopen(request)
    cl = response.read()
    return cl
  except:
    print 'nothing to see here'

def writeToFile(httpRes):
  out = open("htmlTest.html","w")
  out.write(httpRes)
  out.close()
    
httpRes = getRequestResults('http://wausau.craigslist.org/search/sss?sort=rel&minAsk=1000&maxAsk=8000&autoMakeModel=F150&autoMinYear=2004&autoMaxYear=2008&query=F150')
writeToFile(httpRes)
