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
  searchStrings = []
  applicableSites = getSites(vals['zipCode'],vals['searchRadius'])
  searchStrings = getStrings(applicableSites,vals)
  myPages = getRequestResults(searchStrings)    
  
  for myPages in myPages:
    truckVals = parseHTML(myPages['page'],myPages['linkRoot'])
    linkVals.append("<h3>Results from " + myPages['linkRoot'] + "</h6>")
    vals = turnToHTML(truckVals)
    for val in vals:
      linkVals.append(val)
    
  return render_template('base.html', CRS = {'hello':linkVals})
  
def turnToHTML(truckVals):
  linkVals = []
  for entry in truckVals:
    linkString = entry['town'] + " " + entry['price'] + " <a href='" + entry['link'] +"'>" + entry['description'] + "</a><br />";
    linkVals.append(linkString)
  return linkVals