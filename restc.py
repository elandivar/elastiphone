import json
import httplib2 #installed manually

def get_rest_data(http, url_ext, url_int):
   # Retrieve External Contact List
   response1, content = http.request(url_ext, 'GET', body='', headers={'content-type':'text/plain'})
   print response1.status
   data1 = json.loads(content.decode())
   # Retrieve Internal Contact List
   response2, content = http.request(url_int, 'GET', body='', headers={'content-type':'text/plain'})
   data2 = json.loads(content.decode())
   data = {}
   # If HTTP status is not 200 fill data with an empty array to avoid errors when handle the data variable
   if response1 == 200 and response2 == 200:
      data['contacts'] = data1['contacts']
      data['extensions'] = data2['extension']
   else:
      data['contacts'] = {}
      data['extensions'] = {}
   
   return data
