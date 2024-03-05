import urllib.parse
import urllib.request

url = 'http://example.com'
with urllib.request.urlopen(url) as response: # GET REQUEST
    content = response.read()

print(content)
