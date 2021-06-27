import requests

url = 'http://localhost:8080/nfe'
response = requests.get(url)

print(response.status_code)
print(response.text)

