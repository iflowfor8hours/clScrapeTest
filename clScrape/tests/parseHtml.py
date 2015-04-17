from HTMLParser import HTMLParser
from lxml import html
import requests
import re

def getPage(pageFile):
  f = open(pageFile, 'r')
  reader = f.read()
  return reader

truckVals = []
trucksObj = {}
myPage = getPage('htmlTest.html')
tree = html.fromstring(myPage)

trucks = tree.xpath('//div[@class="content"]/p[@class="row"]')

trucksObj['price'] = trucks[0].xpath('//span[@class="price"]/text()')
trucksObj['date'] = trucks[0].xpath('//time/@datetime')
trucksObj['town'] = trucks[0].xpath('//span[@class="pnr"]/small/text()')
trucksObj['link'] = trucks[0].xpath('//span[@class="pl"]/a/@href')
trucksObj['id'] = trucks[0].xpath('//span[@class="pl"]/a/@data-id')
trucksObj['description'] = trucks[0].xpath('//span[@class="pl"]/a/text()')

reg = re.compile('^http')
for x in xrange(0,len(trucksObj['id'])):
  if(trucksObj['link'][x].startswith('http')):
     pass #removes non-local (duplicate) results
  else:  
    tObj = {'price': trucksObj['price'][x],
            'date': trucksObj['date'][x],
            'town': trucksObj['town'][x],
            'link': trucksObj['link'][x],
            'id': trucksObj['id'][x],
            'description': trucksObj['description'][x]
           }
    truckVals.append(tObj)

for t in truckVals:
  print str(t)
#print(trucks)

'''
              <p class="row" data-pid="4975432621"> 
                <a href="/ctd/4975432621.html" class="i" data-ids="0:01313_2jFnYlruCRm,0:00Q0Q_a7XUWBFbp5d,0:00v0v_i1EvJg3UCKO,0:00M0M_945dbZTKX6j,0:00Y0Y_5PWOiA0IIYg,0:00D0D_jgUNo0byaFE,0:00A0A_OFvGqUzgwX,0:00b0b_84iEJzYz1af,0:00s0s_eQUeKVgGSKk,0:00c0c_2Wa1NhiSPDz,0:00N0N_gp3tKwfYJIo,0:00W0W_auTGcATzvlH,0:00J0J_llDpnlIgxfy,0:00w0w_6PFD4s69ozk,0:00C0C_9O7TreEwnYl">
                   <span class="price">&#x0024;6950</span>
                </a> 
                <span class="txt"> 
                  <span class="star"></span> 
                  <span class="pl"> 
                    <time datetime="2015-04-12 12:11" title="Sun 12 Apr 12:11:03 PM (3 days ago)">Apr 12</time> 
                    <a href="/ctd/4975432621.html" data-id="4975432621" class="hdrlnk">2005 FORD F150 XLT SUPER CAB EXCEPTIONAL CONDITION</a> 
                  </span> 
                  <span class="l2"> 
                    <span class="price">&#x0024;6950</span> 
                    <span class="pnr"> 
                      <small> (MONTELLO)</small> 
                      <span class="px"> 
                        <span class="p"> pic</span>
                      </span> 
                    </span> 
                    <a class="gc" href="/ctd/" data-cat="ctd">cars &amp; trucks - by dealer</a> 
                  </span> 
                </span> 
              </p>
              
class MyHTMLParser(HTMLParser):
  
  def __init__(self):
    HTMLParser.__init__(self)
    self.recording = 0
    self.data = []
    self.dataObj = {}
    
  def handle_starttag(self, tag, attrs):
    self.recording = 1
    self.dataObj['tag'] = tag
    self.dataObj['attrs'] = attrs
  def handle_endtag(self, tag):
    self.recording -= 1
  def handle_data(self, data):
    if self.recording:
      self.dataObj['data'] = data
      self.data.append(self.dataObj)

def getPage(pageFile):
  f = open(pageFile, 'r')
  reader = f.read()
  return reader

myPage = getPage('htmlSample.html')
parser = MyHTMLParser()
parser.feed(myPage)

data = parser.data

for x in data:
  print x
  print "BREAK"

'''