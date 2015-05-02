import os, json, re
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify
from werkzeug import secure_filename

app = Flask(__name__, static_url_path='')
  
#is it possible to do a redirect after python has done it's thing???
@app.route('/',methods=['POST'])
def setFunction():
  inputType = request.form['inputType']
  if(inputType == 'GetValues'):
    from clScrape.getValues import getAppSites
    myResults = getAppSites(app,request.form)
    
  else:
    print inputType + ": not found"
  return myResults

@app.route('/siteResults',methods=['POST'])
def getValues():
  from clScrape.getValues import getValues
  reg = re.compile('\[(.*)\]$')
  vals = request.form.keys()
  valsToPass = {}
  for x in vals:
    key = reg.search(x)
    myKey = key.group(1)
    myVal = request.form[x]
    valsToPass[myKey]=myVal
    
  results = getValues(app,valsToPass)
  return jsonify({'site':results})
  
if __name__ == 'main':
  app.run()

def register_blueprints(app):
  from clScrape.views import pages
	
  app.register_blueprint(pages)

register_blueprints(app)