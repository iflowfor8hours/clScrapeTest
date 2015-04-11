import os, csv, pymongo, time
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify
from werkzeug import secure_filename

app = Flask(__name__, static_url_path='')

#is it possible to do a redirect after python has done it's thing???
@app.route('/',methods=['POST'])
def setFunction():
  inputType = request.form['inputType']
  '''
    if(inputType == 'upload'):
    from housing.upload import upload
    results = upload(app)
  
  elif(inputType == 'CurrentRentStatus'):
    from housing.crs import crs
    currentMonth = time.strftime("%b:%Y")
    (month,year) = currentMonth.split(':',1)
    timeFrame = {'startMonth':month,'endMonth':month,'startYear':year,'endYear':year,'msg':'CRS'}
    results = crs(app,timeFrame)
  '''
  if(inputType == 'GetValues'):
    from clScrape.getValues import getValues
    results = getValues(app)
  else:
    print inputType + ": not found"
    
  return results

if __name__ == 'main':
  app.run()

def register_blueprints(app):
  from clScrape.views import pages
	
  app.register_blueprint(pages)

register_blueprints(app)