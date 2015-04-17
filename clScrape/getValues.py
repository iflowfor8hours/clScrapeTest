from flask import Flask, render_template, jsonify
from lxml import html
import requests
import re
from urllib2 import Request, urlopen, URLError
import json
import csv
import math

def getValues(app,vals):
  truckVals = []
  linkVals = []
  applicableSites = []
  searchStrings = []
  applicableSites = getSites(vals['zipCode'],vals['searchRadius'])
  #TODO Get Base Search String
  #Building a pretty bad way to do this now, should be revisited next week
  #should be able to build a much better combinator-inator :)
  for ap in applicableSites:
    for make, value in vals.iteritems():
      searchString = "http://" + ap + ".craigslist.org/search/sso?"
      if value == 'make':
        searchStringMake = searchString + "autoMakeModel=" + make +"+"
        searchStringComplete = searchStringMake
        for model, value in vals.iteritems():
          if value == 'model':
            searchStringModel = searchStringMake + model +"&"
            searchStringComplete = searchStringModel
            if(vals['minYear']):
              searchStringComplete = searchStringComplete + "autoMinYear=" + vals['minYear'] + "&"
            if(vals['maxYear']):
              searchStringComplete = searchStringComplete + "autoMaxYear=" + vals['maxYear'] + "&"
            
            searchStringComplete = searchStringComplete + "query="
            if(vals['knock']):
              searchStrings.append(searchStringComplete + "knock")
            if(vals['cam phasers']):
              searchStrings.append(searchStringComplete + "cam+phasers")
            if(vals['5.4 engine']):
              searchStrings.append(searchStringComplete + "5.4+engine")
            if(vals['needs']):
              searchStrings.append(searchStringComplete + "needs")
            if(vals['needs work']):
              searchStrings.append(searchStringComplete + "needs+work")
            if(vals['needs engine']):
              searchStrings.append(searchStringComplete + "needs+engine")
            if(vals['needs new engine']):
              searchStrings.append(searchStringComplete + "needs+new engine")
            if(vals['5.4L']):
              searchStrings.append(searchStringComplete + "5.4L")
          
  print searchStrings
  #TODO Get Specific Keywords
  #TODO Loop through each site and loop through with each set of keywords
  
  linkRoot = "http://wausau.craigslist.org"
  print str(vals)
  myPage = getPage('htmlTest.html')
  #make this whole thing a for loop... go through all the iterations...
  #may have to turn the myPage to text
  truckVals = parseHTML(myPage,truckVals,linkRoot)
  #end Loop Here
  linkVals.append("<h3>Results from " + linkRoot + "</h6>")
  vals = turnToHTML(truckVals)
  for val in vals:
    linkVals.append(val)
    
  #DELETE THIS
  linkVals.append(applicableSites)
  #-----------------------------
  return render_template('base.html', CRS = {'hello':linkVals})

def getSites(zipCode,radius):
  csvFile = 'zipcode.csv'
  clFile = 'clData.csv'
  acceptableSites = []
  zipObj = zipIt(zipCode,csvFile)
  clList = getCL(clFile)

  for c in clList:
    distance = distance_on_unit_sphere(c["LAT"], c["LON"], zipObj["LAT"], zipObj["LON"])
    if(float(distance) < float(radius)):
      acceptableSites.append(c['hostname'])
  
  return acceptableSites

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
  degrees_to_radians = math.pi/180.0
       
  # phi = 90 - latitude
  phi1 = (90.0 - lat1)*degrees_to_radians
  phi2 = (90.0 - lat2)*degrees_to_radians
         
  # theta = longitude
  theta1 = long1*degrees_to_radians
  theta2 = long2*degrees_to_radians
  
  cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
         math.cos(phi1)*math.cos(phi2))
  arc = math.acos( cos )
 
  #To get the distance in miles, multiply by 3960. 
  #To get the distance in kilometers, multiply by 6373.
  arc = arc * 3960 #miles
  return arc 

def parseHTML(myPage,truckVals,linkRoot):
  trucksObj = {}
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
              'link': linkRoot + trucksObj['link'][x],
              'id': trucksObj['id'][x],
              'description': trucksObj['description'][x]
             }
      tObj['town']= tObj['town'].replace('(','')
      tObj['town']= tObj['town'].replace(')','')
      truckVals.append(tObj)
  return truckVals
  
def turnToHTML(truckVals):
  linkVals = []
  for entry in truckVals:
    linkString = entry['town'] + " " + entry['price'] + " <a href='" + entry['link'] +"'>" + entry['description'] + "</a><br />";
    linkVals.append(linkString)
  return linkVals

def getPage(pageFile):
  f = open(pageFile, 'r')
  reader = f.read()
  return reader

'''
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

'''