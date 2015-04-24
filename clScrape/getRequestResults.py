from urllib2 import Request, urlopen, URLError
from threading import Thread
from Queue import Queue
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s_ %(message)s',
                    )
pageQueue = Queue()
pageObjs = []

def getRequestResults(sites):
  sortedObjs = []
  for i in range(len(sites)):
    t = Thread(target=gotoSite, args=(pageQueue,))
    t.setDaemon = True
    t.start()
  for s in sites:
    pageQueue.put(s)
  
  pageQueue.join()
  #sort by location
  sortedObjs = sorted(pageObjs, key=lambda k: k['linkRoot'])
  return sortedObjs

def gotoSite(q):
  while True:
    site = q.get()
    logging.debug("Loading: %s" % site['string'] )
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
    logging.debug("Processed: %s" % site['string'] )
    q.task_done()

