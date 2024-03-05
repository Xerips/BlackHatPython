# Networking Tools

All of the scripts have comments to break down what is going on. First look at the script code then look  
through this.  

### NetCat.py

You can use the original nc with this script as well, though this script is less stable than nc and should  
only be used when nc cannot (not present, no installation privs).  

A basic NC clone.  
For usage instructions:  
```python3 NetCat.py --help ```  
  
When using NetCat.py for a reverse shell, remember to press Ctrl+D to send the end-of-file (EOF).  
This will open the command prompt.  
  
More usage examples:  
```
python3 NetCat.py -t $IP -p 5555 -l -e="cat /etc/passwd" # this sets up the listener to send the contents of /etc/passwd when someone connects.  
  
echo -ne "GET / HTTP/1.1\r\nHost: <target>.com\r\n\r\n" |python3 ./NetCat.py -t <target>.com -p 80 # Send a GET request to a website to get server info.

```

### TCPproxy.py

A simple proxyserver that will print out the hex and printable characters between a local host and a remote  
host.  
This can be useful to see password written in plaintext (if the protocol is plaintext - like ftp)  
It's a proxy. Think BurpSuite, but without the fancy plugins and tools.  
  
run python3 TCPproxy.py with no arguments for a usage example.  
  
### TCPclient.py, TCPserver.py, and UDPclient.py

Very simple scripts. Best used for testing, simple tasks, or for copy pasting functionality into more complex scripts.  
