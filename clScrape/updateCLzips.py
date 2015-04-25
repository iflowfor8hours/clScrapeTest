from urllib2 import Request, urlopen, URLError
import json
import csv

#NOT DIRECTLY PART OF THE WEBSITE
#Run this script separately if the craigslist sites change names. 
#It will update the CSV used to determine sites in the radius

def getClSites():
  request = Request('http://www.craigslist.org/about/areas.json')
  try:
    response = urlopen(request)
    clSites = response.read()
    cList = json.loads(clSites)
    return cList
  except URLError, e:
    print 'Nothing good out here, error is:', e

def writeToCSV(cld):
  with open('clData.csv','w') as csvfile:
    clWriter = csv.writer(csvfile,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
    for c in cls:
      clWriter.writerow([ c['lat'], c['lon'], c['hostname'], c['name'] ])
      
cls = getClSites()
writeToCSV(cls)
'''
IF YOU WANT TO ADD MORE TO CSV THIS IS THE JSON STRUCT
{"country":"US",
 "lat":"37.500000",
 "region":"CA",
 "name":"SF bay area",
 "lon":"-122.250000",
 "hostname":"sfbay"},                  
'''