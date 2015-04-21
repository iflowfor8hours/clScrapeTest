from urllib2 import Request, urlopen, URLError

def getRequestResults(sites):
  pageObjs = []
  for s in sites:
    print s
    index = s.index('.')
    name = s[7:index]
    request = Request(s)
    try :
      response = urlopen(request)
      cl = response.read()
      pageObjs.append({"linkRoot":"http://" + name + ".craigslist.org","page":cl})
    except:
      print 'nothing to see here'
  return pageObjs    