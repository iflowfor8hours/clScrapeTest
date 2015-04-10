from urllib2 import Request, urlopen, URLError
import json
import csv
import math
import xml.etree.ElementTree as ET

def zipIt(zipcode,csvFile):
  with open(csvFile, mode='r') as infile:
    reader = csv.reader(infile)
    for rows in reader:
      try:
        if( str(rows[0]) == zipcode):
          return {"CITY":rows[1],
                  "STATE":rows[2],
                  "LAT":float(rows[3]),
                  "LON":float(rows[4])
                 }
      except:
        pass #empty row in CSV
  return {"CITY":"UNKNOW","STATE":"UNKNOWN","LAT":0,"LON":0}

def getCL(clFile):
  clList = []
  with open(clFile, mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
      try:
        clList.append({"LAT":float(row[0]),
                       "LON":float(row[1]),
                       "hostname":row[2],
                       "name":row[3]
                      })  
      except:
        print "ERROR WITH ROW" + str(row)
  return clList

def distance_on_unit_sphere(lat1, long1, lat2, long2):
  #from john d cook website http://www.johndcook.com/blog/python_longitude_latitude/
  # Convert latitude and longitude to
  # spherical coordinates in radians.
  degrees_to_radians = math.pi/180.0
       
  # phi = 90 - latitude
  phi1 = (90.0 - lat1)*degrees_to_radians
  phi2 = (90.0 - lat2)*degrees_to_radians
         
  # theta = longitude
  theta1 = long1*degrees_to_radians
  theta2 = long2*degrees_to_radians
         
  # Compute spherical distance from spherical coordinates.
         
  # For two locations in spherical coordinates
  # (1, theta, phi) and (1, theta, phi)
  # cosine( arc length ) =
  #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
  # distance = rho * arc length
     
  cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
         math.cos(phi1)*math.cos(phi2))
  arc = math.acos( cos )
 
  # Remember to multiply arc by the radius of the earth
  # in your favorite set of units to get length.
  #To get the distance in miles, multiply by 3960. 
  #To get the distance in kilometers, multiply by 6373.
  arc = arc * 3960 #miles
  return arc 

def getRequestResults(site):
  request = Request(site)
  try :
    response = urlopen(request)
    cl = response.read()
    print cl
    return cl
  except:
    print 'nothing to see here'

#zipcode,maxDistance, and data variables should come from website, fileLocations should come from args file
maxDistance = 100
zipcode = '54401'
dataVariables = 'sss?sort=priceasc&query=f250'
csvFile = 'zipcode.csv'
clFile = 'clData.csv'

acceptableSites = []

zipObj = zipIt(zipcode,csvFile)
clList = getCL(clFile)

for c in clList:
  distance = distance_on_unit_sphere(c["LAT"], c["LON"], zipObj["LAT"], zipObj["LON"])
  if(distance < maxDistance):
    acceptableSites.append(c)

for a in acceptableSites:
  siteSearch = 'http://' + a["hostname"] + '.craigslist.org/search/' + dataVariables
  print siteSearch

res = getRequestResults(siteSearch)
print res
#request = Request('http://www.realtor.com/realestateandhomes-search/10002')
#list of zipcodes and their geocoords
'''
project notes
wan/4963231518.html
Referer	http://wausau.craigslist.org/search/sss?query=f150%20topper&sort=rel

TO SORT BY PRICE:
http://wausau.craigslist.org/search/sss?sort=priceasc&query=f150%20topper%20unicover%20safari

#space means AND

request = Request('http://www.craigslist.org/about/areas.json')
{"country":"US",
 "lat":"37.500000",
 "region":"CA",
 "name":"SF bay area",
 "lon":"-122.250000",
 "hostname":"sfbay"},                  

try:
    response = urlopen(request)
    clSitesUS = response.read()
    cList = json.loads(clSitesUS)
    for c in cList:
      pass
      #print c['hostname']
except URLError, e:
    print 'Nothing good out here, error is:', e
'''
#open args.txt and read in
#loop requests