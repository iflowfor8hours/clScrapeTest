from lxml import html
import logging

#Parse HTML using xpath, interested in <row>...</row> and <h4>...</h4>

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s_ %(message)s',
                    )

def parseHTML(myPage,linkRoot):
  truckValues = []
  try:
    tree = html.fromstring(myPage)
    #get all rows and the h4 demarcation point (local vs nearby) from full CL page
    trucks = tree.xpath('//div[@class="content"]/p[@class="row"] | //div[@class="content"]/h4[@class="ban nearby"]')
  except:
    logging.debug("Failed to make tree")
    return []
  
  for truck in trucks:
    trucksObj = {}
    flag = 0
    if(truck.tag == "h4"):
      #exit when we have processed all local results
      break
    else:
      #make a new searchable tree (t) for each local truck listing <row> ... </row>
      truck = html.tostring(truck)
      t = html.fromstring(truck)
      try:
        trucksObj['price'] = t.xpath('//span[@class="price"]/text()')[0]
      except:
        trucksObj['price'] = "$0"
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
        flag = 1 #disallow if there is no link
      try:  
        trucksObj['id'] = t.xpath('//span[@class="pl"]/a/@data-id')[0]
      except:
        trucksObj['id'] = '0000'
      try:  
        trucksObj['description'] = t.xpath('//span[@class="pl"]/a/text()')[0]
      except:
        trucksObj['description'] = "NO DESCRIPTION"
      
      if flag == 0 :
        try:
          trucksObj['town']= trucksObj['town'].replace('(','')
          trucksObj['town']= trucksObj['town'].replace(')','')
        except:
          "Couldn't Remove () from (TOWN)"
        truckValues.append(trucksObj)
      else:
        logging.debug("Skipping for malformed data, missing link: %s" % trucksObj )
        
  return truckValues