import urllib.request
import urllib.parse

url = "https://example.com/login"

info = {'user': 'tim', 'passwd': '31337'}
data = urllib.parse.urlencode(info).encode() # Data is now of type bytes.

req = urllib.request.Request(url, data)
with urllib.request.urlopen(req) as response: # POST request.
    content = response.read()

print(content)
