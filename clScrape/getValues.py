from flask import Flask, render_template
from getRequestResults import getRequestResults
from buildStrings import getStrings
from getRangeSites import getSites
from parseHTML import parseHTML

#This is the equivalent of "main" when Search is clicked.

def getAppSites(app,vals):
  applicableSites = []
  applicableSites = getSites(vals['zipCode'],vals['searchRadius']) #Get cl sites within the radius
  #Return to website  
  return render_template('base.html', CRS = {'hello':applicableSites, 'formData':vals})

def getValues(app,vals):
  linkVals = []
  truckVals = []
  progress = vals['progress']  
  searchStrings = getStrings(vals) #Builds url strings to be scraped
  myPages = getRequestResults(searchStrings) #HTML pages from url strings   
  currentRoot = ""
  for myPages in myPages:
    #process all returns from a given cl site, myPages is sorted by linkRoot (wausau.craigslist.org, etc...) 
    if currentRoot == myPages['linkRoot']: 
      pass 
    #once gathered, turn results into html lines, add header line to show where results are from
    else: 
      try:
        values = turnToHTML(truckVals)
        for val in values:
          linkVals.append(val)
        truckVals = []
      except:
        print "Empty val set?"
        truckVals = []
      currentRoot = myPages['linkRoot']
      linkVals.append("<h5>Results from " + myPages['linkRoot'] + "   " + progress + "</h5>")
    
    #parse html pages with xpath/xquery
    tempVals = parseHTML(myPages['page'],myPages['linkRoot'])
    for t in tempVals:
      t['querySet'] = myPages['querySet']
      t['url'] = myPages['url']
      truckVals.append(t)
  
  #Clean up pages from final cl root site (eauclaire.craigslist.org, etc)
  #Same as try directly under else
  try:
    vals = turnToHTML(truckVals)
    for val in vals:
      linkVals.append(val)
  except:
    print "Empty val set"
  
  return linkVals
#Build HTML lines
def turnToHTML(truckVals):
  linkVals = []
  for entry in truckVals:
    if(entry['link'] == "NONE"):
      linkString = "<a href='" + entry['url'] + "'>Connection Failed </a>(" + entry['querySet'] + ")<br />" 
      linkVals.append(linkString)
    else:  
      linkString = entry['town'] + " " + entry['price'] + " <a href='" 
      linkString = linkString + entry['link'] +"'>" + entry['description'] + "</a> (" 
      linkString = linkString + entry['querySet'] + " )<br />";
      linkVals.append(linkString)
  return linkVals