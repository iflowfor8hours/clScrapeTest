from urllib2 import Request, urlopen, URLError
from threading import Thread
from Queue import Queue
import logging
#Go to each URL and get HTML response

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s_ %(message)s',
                    )

def setObjs():
  #Array for the results
  global pageObjs 
  pageObjs = []
  #Queue for the pages
  global pageQueue 
  pageQueue = Queue()
  
def getRequestResults(sites):
  setObjs()
  sortedObjs = []
  #Create a thread for each web page (cap at 50 for testing)
  #To increase or reduce threads, change the 50 value below
  numThreads = min(len(sites),50)
  logging.debug("Using  " + str(numThreads) + " Threads")
  
  for i in range(numThreads):
    t = Thread(target=gotoSite, args=(pageQueue,))
    t.setDaemon = True
    t.start()
  for s in sites:
    logging.debug("SITES %s" %s)
    pageQueue.put(s)
  #wait for queue to process
  pageQueue.join()
  #sort by location
  logging.debug("ENDING LENGTH OF pageObjs: " + str(len(pageObjs)))
  sortedObjs = sorted(pageObjs, key=lambda k: k['linkRoot'])
  return sortedObjs

def gotoSite(q):
  while True:
    #get pages from Queue, while True used so thread count can be restricted if desired
    site = q.get()
    logging.debug("Loading: %s" % site['string'] )
    s = site['string']
    index = s.index('.')
    name = s[7:index]
    request = Request(s)
    try :
      response = urlopen(request, timeout=10)
      cl = response.read()
      pageObjs.append({"linkRoot":"http://" + name + ".craigslist.org","page":cl,"querySet":site['querySet']})
    except:
      print 'nothing to see here'
    #announce process complete
    logging.debug("Processed: %s" % site['string'] )
    q.task_done()

