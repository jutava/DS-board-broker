import requests
  
# api-endpoint 
URL = 'http://localhost:8080'
  
# sending get request and saving the response as response object 
r = requests.get(url = URL) 
  

data = r.text
  
# printing the output 
print(data) 