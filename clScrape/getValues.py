from flask import Flask, render_template, jsonify

def getValues(app,vals):
  return render_template('base.html', CRS = {'hello':str(vals)})
