from flask import Flask, render_template, jsonify
from getRequestResults import getRequestResults
from buildStrings import getStrings
from getRangeSites import getSites
from parseHTML import parseHTML
import requests
import json

def getValues(app,vals):
  linkVals = []
  applicableSites = []
  truckVals = []
  searchStrings = {}
  applicableSites = getSites(vals['zipCode'],vals['searchRadius'])
  searchStrings = getStrings(applicableSites,vals)
  myPages = getRequestResults(searchStrings)    
  currentRoot = ""
  for myPages in myPages:
    if currentRoot == myPages['linkRoot']:
      pass
    else:
      try:
        vals = turnToHTML(truckVals)
        for val in vals:
          linkVals.append(val)
        truckVals = []
      except:
        print "Empty val set? Emptying truckVals"
        truckVals = []
      currentRoot = myPages['linkRoot']
      linkVals.append("<h5>Results from " + myPages['linkRoot'] + "</h5>")
      
    tempVals = parseHTML(myPages['page'],myPages['linkRoot'])
    for t in tempVals:
      t['querySet'] = myPages['querySet']
      truckVals.append(t)
  
  try:
    vals = turnToHTML(truckVals)
    for val in vals:
      linkVals.append(val)
  except:
    print "Empty val set"
  return render_template('base.html', CRS = {'hello':linkVals})
  
def turnToHTML(truckVals):
  linkVals = []
  for entry in truckVals:
    linkString = entry['town'] + " " + entry['price'] + " <a href='" 
    linkString = linkString + entry['link'] +"'>" + entry['description'] + "</a> (" 
    linkString = linkString + entry['querySet'] + " )<br />";
    linkVals.append(linkString)
  return linkVals