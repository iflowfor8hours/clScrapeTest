from flask import Flask, render_template, jsonify
from urllib2 import Request, urlopen, URLError
from buildStrings import getStrings
from getRangeSites import getSites
from lxml import html
import requests
import re
import json

def getValues(app,vals):
  truckVals = []
  linkVals = []
  applicableSites = []
  searchStrings = []
  applicableSites = getSites(vals['zipCode'],vals['searchRadius'])
  searchStrings = getStrings(applicableSites,vals)
  for s in searchStrings:
    print "this is a string: " +s
  
  #----------------------------------------
  #
  # get pages loop here, don't want to get blocked yet, so... simulating for now
  #'''
  myPages = getRequestResults(searchStrings)    
  #'''
  #
  #myPage = getPage('htmlTest.html')
  #linkRoot = "http://wausau.craigslist.org"
  #myPages = [{"linkRoot":linkRoot,"page":myPage}]
  #----------------------------------------
  for myPages in myPages:
    truckVals = parseHTML(myPages['page'],truckVals,myPages['linkRoot'])
    linkVals.append("<h3>Results from " + myPages['linkRoot'] + "</h6>")
    vals = turnToHTML(truckVals)
    for val in vals:
      linkVals.append(val)
    
  #DELETE THIS
  #linkVals.append(applicableSites)
  #booah = getRequestResults(['http://www.littlebooah.com','http://jangmi.littlebooah.com'])
  #for b in booah:
  #  print b['page']
  #-----------------------------
  return render_template('base.html', CRS = {'hello':linkVals})

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

