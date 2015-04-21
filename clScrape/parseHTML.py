from lxml import html

import re

def parseHTML(myPage,linkRoot):
  truckValues = []
  tree = html.fromstring(myPage)
  try:
    trucks = tree.xpath('//div[@class="content"]/p[@class="row"] | //div[@class="content"]/h4[@class="ban nearby"]')
  except:
    print "Failed to make tree"
    return []
  
  for truck in trucks:
    trucksObj = {}
    flag = 0
    if(truck.tag == "h4"):
      print "Breaking for h4"
      break
    else:
      truck = html.tostring(truck)
      t = html.fromstring(truck)
      try:
        trucksObj['price'] = t.xpath('//span[@class="price"]/text()')[0]
      except:
        truckObj['price'] = "$0"
      try:  
        trucksObj['date'] = t.xpath('//time/@datetime')[0]
      except:
        trucksObj['date'] = "NO DATE"
      try:  
        trucksObj['town'] = t.xpath('//small/text()')[0]
      except:
        trucksObj['town'] = "UNKNOWN"
      try:
        link = t.xpath('//span[@class="pl"]/a/@href')[0]
        trucksObj['link'] = linkRoot + link
      except:
        flag = 1
      try:  
        trucksObj['id'] = t.xpath('//span[@class="pl"]/a/@data-id')[0]
      except:
        flag = 1
      try:  
        trucksObj['description'] = t.xpath('//span[@class="pl"]/a/text()')[0]
      except:
        trucksObj['description'] = "NO DESCRIPTION"
      
      if flag == 0 :
        try:
          trucksObj['town']= trucksObj['town'].replace('(','')
          trucksObj['town']= trucksObj['town'].replace(')','')
        except:
          "Couldn't Remove () from town"
        truckValues.append(trucksObj)
      else:
        print "Skipping for malformed data " + str(trucksObj)
        
  return truckValues