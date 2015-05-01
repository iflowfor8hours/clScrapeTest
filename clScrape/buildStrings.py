#Builds the URL string to be scraped
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s_ %(message)s',
                    )

def getStrings(vals):
  finalStringList = []
  
  stringList = ["http://" + vals['site'] + ".craigslist.org/search/sso?"]
  stringList = getMake(stringList,vals)
  stringList = getModel(stringList,vals)
  stringList = getYears(stringList,vals)
  stringList = getPrice(stringList,vals)
  stringList = getKeyWords(stringList,vals)
  for s in stringList:
    #string is the url, querySet is the keyword argument used ("5.4","needs", etc)
    finalStringList.append({'string':s[0],'querySet':s[1]})
  logging.debug("FINAL STRING LIST " + str(finalStringList)) 
  return finalStringList

#make and model are queried using autoMakeModel=X X could be [MAKE or MODEL or MAKE+MODEL]
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

#years are queried using "autoMinYear=YEAR" and "autoMaxYear=YEAR"
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

#prices are queried using "minAsk=PRICE" and "maxAsk=PRICE"
def getPrice(searchStrings,vals):
  returnList = []
  if(vals['minPrice'] or vals['maxPrice']):
    if(searchStrings[0].find("=")>0):
      for s in searchStrings:
        if(vals['minPrice']):
          s = s + "&" + "minAsk=" + vals['minPrice']
        if(vals['maxPrice']):
          s = s + "&" + "maxAsk=" + vals['maxPrice']
        returnList.append(s)
    else:
      for s in searchStrings:
        if(vals['minPrice']):
          s = s + "minAsk=" + vals['minPrice']
          if(vals['maxPrice']):
            s = s + "&" + "maxAsk=" + vals['maxAsk']
        elif(vals['maxPrice']):
          s = s + "maxAsk=" + vals['maxPrice']
        returnList.append(s)
       
  if(len(returnList)>0):
    return returnList
  return searchStrings

#keywords are queried using "query=X" wher x is [QUERY or "QUERY+QUERY2"(for ANDING)]
#keywords are passed back for use in html string
def getKeyWords(stringList,vals):
  returnList = []
  for s in stringList:
    if(s.find('=')>0):
      s = s + "&"
    s = s + 'query="'
    for keywords, value in vals.iteritems():
      if value == 'keywords':
        keywords = keywords.replace(" ","+")
        returnList.append([s + keywords +'"',keywords])  
  if(len(returnList)>0):
    return returnList
  else:
    for s in stringList:
      returnList.append([s,""])
  return returnList
