import csv
import math
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s_ %(message)s',
                    )
#Returns a list of CL sites within X miles of zip code Y
#Zip code and radius provided by user on web page
#CL site info and zipcode info stored in CSV files

def getSites(zipCode,radius):
  csvFile = 'zipcode.csv'
  clFile = 'clData.csv'
  acceptableSites = []
  sortedObjs = []
  sortedSites = []
  zipObj = zipIt(zipCode,csvFile)
  clList = getCL(clFile)

  for c in clList:
    distance = distance_on_unit_sphere(c["LAT"], c["LON"], zipObj["LAT"], zipObj["LON"])
    if(float(distance) < float(radius)):
      acceptableSites.append({'name':c['hostname'],'distance':distance})
  logging.debug("ACCEPTABLE SITES: %s" % acceptableSites)
  
  sortedObjs = sorted(acceptableSites, key=lambda k: float(k['distance']))
  for s in sortedObjs:
    sortedSites.append(s['name'])
  
  return sortedSites

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
