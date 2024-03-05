# Scapy

Scapy is a python library which packs a serious punch when it comes to working with packets.  
  
Scapy was designed to work on linux and windows, but given the choice, it's best to work with it in a linux environment as it was originally designed to work in that environment (you could use arch, btw).  
  
We installed Scapy on our system using ```sudo pac -S scapy```, you could also install it in your venv if you wanted to localize it to your project, or use a different package manager if you're using a different distribution of linux. This gives us the library which we can use globally in any project, but also the Scapy tool itself to use standalone.  
  
Check out [Scapy](https://scapy.net/). It's more than a just a library!  

The "sniff" function in Scapy looks like the following:  
  
```sniff(filter='',iface="any",prn=function,count=N```  
  
The "filter" parameter allows up to specify which Berkeley Packet Filter for the sniffer to sniff. Leaving it blank will sniff all packets.  
The "iface" parameter allows us to specify which network interface to sniff on.  
The "prn" parameter specifies a callback function to be called for every packet that matches the filter, and the callback function receives the packet object as its single parameter.  
The "count" parameter specifies how many packets you want to sniff. If left blank it will sniff indefinitely.  

### mail_sniffer.py

In this tool you can see how much heavy lifting scapy does. Comparing this to our previously made sniffer tools in Sniffer/ really highlights this.  
The book mentions how using *show* in our ```print(packet.show())``` is a great way to debug scripts as you're going along to make sure you're capturing the output you want.  
The basic script to sniff a packet:  
```
from scapy.all import sniff

def packet_callback(packet):
    print(packet.show())

def main():
    sniff(prn=packet_callback, count=1)

if __name__ == '__main__':
    main()
```
That's it!  

On top of this basic script, we can add in logic to peel out email-related authentication strings using Berkeley Packet Filter (BPF) syntax (also called Wireshark style). This syntax is also common to tcpdump and of course, Wireshark.  
  
**BPF Syntax:**  
|Expression|Description|Sample filter keywords|
|----------|-----------|----------------------|
|Descriptor|What you are looking for|host, net, port|
|Direction|Direction of travel|src, dst, src or dst|
|Protocol|Protocol used to send traffic|ip, ip6, tcp, udp|

As you would expect using ```src 192.168.0.1``` will filter all packets to those originating from 192.168.0.1, ```dst 192.168.0.1``` will filter for all of the packets destined for 192.168.0.1.  
You can add the filter keywords to refine your filter. ```tcp port 25``` to filter all tcp packets transmitted over port 25.  

Why/When: You're sitting in your target system and want to lay some snoops down to see if you can catch any creds or useful information from mail servers. Change or add port 21 to get the plain text creds off of ftp. You will only get the creds from protocols that handle credentials in plain text.  

### arper.py

Check out some material on [ARP poisoning](https://www.varonis.com/blog/arp-poisoning).  
If you're working in Arch linux the arp command (along with net-tools) was depricated some time ago in favour of ip neighbour (along with ip).  
You will want a handle on how to use these tools when working on arp poisoning, so I'll give a brief breakdown below to familiarize you with the differences.  

It is important to note that ARP poisoning only works on IPv4 addresses. The Secure Neighbour Discovery (SEND) Protocol prevents an attacker from abusing NDP or ARP to trick hosts into sending traffic that was destined for someone else to the attacker.  
  
**How it works:**  
  
**General + Why/When:**  
  
The tool sets up an Man In The Middle (MITM) attack to capture packets on a target system and writes the packets it captures to a .pcap file.  
You've got a shell on a system and want to start capturing packets to see what the system is talking to, accessing, if it's sending plain text creds anywhere, etc.  
  
def poison(self):  
1. Create a poisoned ARP packet intended for the victim and one intended for the gateway.  
2. We send the gateway a packet with the victims IP and the attackers MAC.  
3. We send the victim a packet with the gateways IP and the attackers MAC.  
4. We do this continuously in a loop to ensure the arp cache entries remain poisoned during the attack.  
5. When we exit the attack with Ctrl+c, we restore things to normal. Nothing to see here...  
  
def sniff(self, count=200):  
1. We sniff the network traffic during the attack to see and record whats happening.  
2. We save the packets into a pcap file (arper.pcap)  
3. Restore arp tables to original values and terminate the poison thread.  
  
def restore(self):  
1. Runs when either the poisoning is interrupted with Ctrl+c or the count for sniff is exhausted.  
2. Sends the original values of the victim to the gateway and the original values of the gateway to the victim.  
* During the attack, you can use a terminal to see the poisoned arp cache with: ```arp -a``` or ```ip neigh show```.  
* After the attack, you will notice the .pcap file in the same directory as your arper.py tool.  
  
arper.py takes 3 arguments. Argv[1] = victim, argv[2] = gateway, argv[3] = interface.  Example:  
```python3 arper.py 192.168.1.49 192.168.1.254```  
  
**arp**  
Display entries for a specific interface:  
```arp -i <interface>```  
Display entries for a specific address:  
```arp -a <IPv4 address>```  
Add a new entry (perminently):  
``` arp -s <IPv4 address> -i <interface> <MAC>```  
Removing an entry:  
```arp -d <IPv4 address>```  
  
**ip neigh**  
You can use either ip neighbour or ip neigh.  
Show the current arp table entries:  
```ip neigh show``` In addition to what you get with arp -a, you also receive the system state (reachable, permanent, stale, delay).  
Add a new entry:  
```ip neigh add <IPv4 address> dev <interface>``` "dev" stands for device and is always connected to ```<interface>```.  
Removing an entry:  
```ip neigh del <IPv4 address> dev <interface>```  

### recapper.py and detector.py

Not going to lie, things are about to get a little more technical, and much more creepy! These two tools work in concert to fish out images of peoples faces from pcap files.  

This tool uses named tuple data structures, click [Here](https://www.geeksforgeeks.org/namedtuple-in-python/) for more information on named tuples.  
  
The authors decided to store their pcaps, images, etc, in the /root directory. I don't use the root user on my system unless necessary (practically never after setup), and so I operate out of the /$USER directory (for security reasons and to ensure I don't break something that only the root user can break). This is generally a good practice while using linux and I recommend doing the same.  
  
Change the directories to ones you like. Recapper is setup exactly like the book, detector.py is an example of how I might set up the directories.  
  
**Why/When:**  

You've been tasked with discovering whether a HVT is hiding out in an undisclosed location that your team has been able to gain access to. You know the system you've compromised is being used for web communications over unencrypted http, and it's up to you to confirm if the target is at the location. You fire up your machine, ssh into the target, and start running you're arper.py script to capture all the nefarious goings on to be found on the system. After capturing a veritable mountain of intel, you run the pcap file you've collected through you're facial recognition, suit recapper.py and detector.py, and it's a hit! You see that you've gotten an image file of the targets face, it looks like they've been using the webcam while you were capturing their traffic. They're at the location! Reapers are go, execute, execute!  
  
Note: If you're calling in a drone strike using this type of attack, you may want to actually look through the packets to see what's going on. You'd hate to find out that it was someone looking up pictures of your HVT on an outdated browser which caused the false positive and made you believe they were at the location.  
  
Okay, honestly, these tools are better used as platforms to help you create other tools that capture and interact with packets. Although these tools might seem a little too James Bond to be of any everyday practical use, learning how to work with network packets using these tools and tools like wireshark is incredibly powerful. As Chris Greer is oft to mention, "Packets don't lie." Check out his youtube channel for a plethora of [great content](https://www.youtube.com/channel/UCHN1aYRP473xX6Z13H_mxMQ)!  
  
#### recapper.py

**How it works:**  
  
def get_header(payload):  
1. Takes the raw HTTP traffic and spit out the headers. These start at the beginning and end with a couple carriage returns:  
```header_raw = payload[:payload.index(b'\r\n\r\n')+2]```  
2. If the payload doesn't match the pattern (ValueError), we write a - to the console. If it does match, we create a dictionary, split the header on the colon so that the key is the part before the colon and the value is the part after the colon.  
```header = dict(re.findall(r'(?P<name>.*?): (?P<value>.*?)\r\n', header_raw.decode()))```  
3. If the header doesn't contain the value 'Content-Type', we return None because it doesn't contain the content we want to extract.  
  
def extract_content(Response, content_name='image')  
1. Takes the HTTP response and the name of the content type to isolate images. Response is our namedtuple, header and payload.  
2. If the content has been encoded with gzip or deflate, we decompress the content with the zlib module.  
3. Send the data to two variables: content_type (to store the "image" content type) and content (to store the content itself).  
4. Return a tuple of the content and content_type.  
  
class Recapper:  
1. Initialize the object with the name of the pcap file we want to read. ```pcap = rdpcap(fname)```  
2. Utilize Scapy's automatic separation of each TCP session into complete TCP streams. ```self.sessions = pcap.sessions()```  
3. Create an empty list called ```responses``` that we fill with the responses from the pcap file. ```self.responses = list()```  
  
def get_responses(self):  
1. Iterate over the sessions dictionary, and then the packets within each sessions, filtering for packets sent to destination or source port 80.  
2. Concatenate the filtered traffic into a single buffer called payload and if there is no TCP in the packet, we print an x to console and keep going.  
3. If the ```payload``` byte string is not empty, we pass it to the HTTP-parsing function ```get_header``` to be able to inspect the HTTP headers individually, and append the ```Response``` to the responses list.  
  
def write(self, content_name):  
1. Iterates over the responses, extracts the content, writes the content to a file.  
2. The file is output to the ```OUTDIR``` directory.  

#### detector.py

For this tool to run, you will need to have [OpenCV](https://opencv.org/) installed on your system or installed into the venv of the project.  
  
You will also need a facial detection training file, you can get one here: wget http://eclecti.cc/files/2008/03/haarcascade_frontalface_alt.xml. Put this file in the directory specified in the TRAIN variable.  
  
**How it works:**  
  
Detects faces in the ```ROOT``` variable's directory based on it's training file found in the ```TRAIN``` variable. Writes the recognized images (faces) to the ```FACES``` variable's directory with a rectangle around the face for inspection.  
  
Because it's a pretty short and sweet script thanks to OpenCV, I've made notes in the code to help understand it instead of writing it out here.  

