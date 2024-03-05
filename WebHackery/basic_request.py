import requests
url = 'http://example.com'
    response = requests.get(url) # GET request.

data = {'user': 'tim', 'passwd': 'sekret'}
response = requests.post(url, data=data) # POST request.
    content = response.read()

print(content)
