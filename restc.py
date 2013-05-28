import json
import httplib2 #installed manually

def get_rest_data(http, url_ext, url_int):
   # Retrieve External Contact List
   response, content = http.request(url_ext, 'GET', body='', headers={'content-type':'text/plain'})
   data1 = json.loads(content.decode())
   # Retrieve Internal Contact List
   response, content = http.request(url_int, 'GET', body='', headers={'content-type':'text/plain'})
   data2 = json.loads(content.decode())
   data = {}
   data['contacts'] = data1['contacts']
   data['extensions'] = data2['extension']
   return data
