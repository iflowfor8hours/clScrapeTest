from flask import Flask, render_template, jsonify

def getValues(app):
  return render_template('base.html', CRS = {'hello':'world'})
'''
def crs(app, timeFrame):
  months = {"JAN":"00", "FEB":"01", "MAR":"02", "APR":"03", "MAY":"04", "JUN":"05", "JUL":"06", "AUG":"07", "SEP":"08", "OCT":"09", "NOV":"10", "DEC":"11"}
  rent = MonthlyRentEntries.objects.all()
  completionMessage = []
  #create easy compare date strings. For example: 201400, 201401 for JAN 2014 and FEB 2014
  startDate = timeFrame['startYear'] + months[timeFrame['startMonth'].upper()]
  endDate = timeFrame['endYear'] + months[timeFrame['endMonth'].upper()]

  for rent in rent:
    docDate = str(rent.year) + months[rent.month.upper()]
    if(int(docDate) >= int(startDate) and int(docDate)<= int(endDate)):
      completionMessage.append(rent)
      #print "FOUND ENTRY FOR: " + docDate +"\n"
  if(len(completionMessage) == 0):
    completionMessage.append("No Entry Found From " + timeFrame['startMonth'] + " " + timeFrame['startYear'] + " through " + timeFrame['endMonth'] + " " + timeFrame['endYear']);
  else:
    pass
    #This is the area to gather specific data for CRS, YTD, CUSTOM
    #For example if I want an on-click in the table to do different things based on previous screen click
    #Also we can do preprocessing instead of doing it on the JS side if desired
  return render_template('base.html', CRS = {'type':timeFrame['msg'],'msg':completionMessage, 'option':'none',
                                             'fromDate':timeFrame['startMonth'] + ' ' + timeFrame['startYear'],
                                             'untilDate':timeFrame['endMonth'] + ' ' + timeFrame['endYear']
                                            })
'''