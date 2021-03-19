import requests
import json
URL = 'http://localhost:8080'
data =  { "state" : 1, "x" : 2, "y" : 5, "color" : "WHITE"}

r = requests.post(url = URL, data=json.dumps(data)) 
data = r.text
print("POST Returned:",data)

r = requests.get(url = URL) 
data = r.text
print("GET Returned:",data)