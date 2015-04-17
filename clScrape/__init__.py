import os, csv
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify
from werkzeug import secure_filename

app = Flask(__name__, static_url_path='')

#is it possible to do a redirect after python has done it's thing???
@app.route('/',methods=['POST'])
def setFunction():
  inputType = request.form['inputType']
  if(inputType == 'GetValues'):
    from clScrape.getValues import getValues
    myResults = getValues(app,request.form)
    
  else:
    print inputType + ": not found"
    
  return myResults

if __name__ == 'main':
  app.run()

def register_blueprints(app):
  from clScrape.views import pages
	
  app.register_blueprint(pages)

register_blueprints(app)