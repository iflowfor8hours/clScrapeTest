def getStrings(applicableSites, vals):
  finalStringList = []
  for ap in applicableSites:
    stringList = ["http://" + ap + ".craigslist.org/search/sso?"]
    stringList = getMake(stringList,vals)
    stringList = getModel(stringList,vals)
    stringList = getYears(stringList,vals)
    stringList = getKeyWords(stringList,vals)
    for s in stringList:
      finalStringList.append(s)
  
  return finalStringList

def getMake(searchStrings,vals):
  returnList = []
  for make, value in vals.iteritems():
    if value == 'make':
      returnList.append(searchStrings[0] + "autoMakeModel=" + make)
  if(len(returnList)>0):
    return returnList
  return searchStrings

def getModel(searchStrings, vals):
  returnList = []
  for model, value in vals.iteritems():
    if value == 'model':
      for s in searchStrings:
        if(s.find("autoMakeModel=")>0):
          returnList.append(s + "+" + model)
        else:
          returnList.append(s + "autoMakeModel=" + model) 
  if(len(returnList)>0):
    return returnList
  return searchStrings

def getYears(searchStrings,vals):
  returnList = []
  if(vals['minYear'] or vals['maxYear']):
    if(searchStrings[0].find("=")>0):
      for s in searchStrings:
        if(vals['minYear']):
          s = s + "&" + "autoMinYear=" + vals['minYear']
        if(vals['maxYear']):
          s = s + "&" + "autoMaxYear=" + vals['maxYear']
        returnList.append(s)
    else:
      for s in searchStrings:
        if(vals['minYear']):
          s = s + "autoMinYear=" + vals['minYear']
          if(vals['maxYear']):
            s = s + "&" + "autoMaxYear=" + vals['maxYear']
        elif(vals['maxYear']):
          s = s + "autoMaxYear=" + vals['maxYear']
        returnList.append(s)
       
  if(len(returnList)>0):
    return returnList
  return searchStrings

def getKeyWords(stringList,vals):
  returnList = []
  for s in stringList:
    if(s.find('=')>0):
      s = s + "&"
    s = s + 'query="'
    for keywords, value in vals.iteritems():
      if value == 'keywords':
        keywords = keywords.replace(" ","+")
        returnList.append(s + keywords +'"')  
  if(len(returnList)>0):
    return returnList
  return stringList
