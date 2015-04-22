from urllib2 import Request, urlopen, URLError

def getRequestResults(sites):
  pageObjs = []
  for site in sites:
    print "Checking: " + str(site['string'])
    s = site['string']
    index = s.index('.')
    name = s[7:index]
    request = Request(s)
    try :
      response = urlopen(request)
      cl = response.read()
      pageObjs.append({"linkRoot":"http://" + name + ".craigslist.org","page":cl,"querySet":site['querySet']})
    except:
      print 'nothing to see here'
  return pageObjs    