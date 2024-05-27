# Black Hat Python (BHP):

If you're interested in some Arch Linux ricing and system building, check out my repo on [Arch Linux](https://github.com/Xerips/ArchLinux/)!

## Python Programming for Hackers and Pentesters, 2nd Edition.

Here you'll find all of the tools and scripts found in the book "Black Hat Python."

I've done this for a few reasons:

1. Writing out the tools and experimenting with them/getting them to work, is good for familiarizing yourself with security/network focused python.
2. Writing out detailed descriptions of how the code works really helps to cement python fundamentals.
3. I plan to use these tools and want to iterate on some of them for future use. This repo helps me to do that without having to go through the book (again).
4. Getting into cybersecurity is hard! It can sometimes feel like you can't know anything until you know everything. Seeing as knowing everything is out of the question for us mere mortals, learning how to figure things out and build solutions is the next best thing. Books like BHP endeavor to help you do just that!

- Click around, I hope you enjoy what I've done here or at least find it handy!

Notes before you get started:

- The readme of each directory should provide all the information you'll need for using the tools located there.
- I've written comments in the code as well to identify particularly useful, tricky, or important sections.
- All of the requirements can be installed using pip in a virtual environment for each project.
- I prefer to install most requirements globally using pacman (or apt, homebrew, etc). This means less installing of virtual environments and managing them.
  - This also makes it easier for me to keep things up to date, and I don't have to worry as much about dependencies when I grab an exploit.py or POC.py off of github (or wherever) for a particular vulnerability I'm trying to exploit.

**Disclaimer**

- This project contains potentially harmful code. Please do not use any of this code on a target machine without permission from the owner.
- This project is for educational purposes only and is not intended to be used for criminal activity.
- Have fun with hacking!

## Table of Contents:

### [Basic Networking Tools](https://github.com/Xerips/BlackHatPython/tree/main/BasicNetworkingTools)

### [Sniffer](https://github.com/Xerips/BlackHatPython/tree/main/Sniffer)

### [Scapy](https://github.com/Xerips/BlackHatPython/tree/main/Scapy)

### [Web Hackery](https://github.com/Xerips/BlackHatPython/tree/main/WebHackery)

### [Extending Burp](https://github.com/Xerips/BlackHatPython/tree/main/ExtendingBurp)

### [GitHubTrojan](https://github.com/Xerips/BlackHatPython/tree/main/GitHubTrojan)

### [Trojaning Tasks for Windows](https://github.com/Xerips/BlackHatPython/tree/main/TrojaningTasksWin)

### [Fun With Exfiltration](https://github.com/Xerips/BlackHatPython/tree/main/FunWithExfil)

### [Windows Priv Esc](https://github.com/Xerips/BlackHatPython/tree/main/WindowsPrivEsc)

### [Offensive Forensics](https://github.com/Xerips/BlackHatPython/tree/main/OffensiveForensics)

## Tips and Tricks:

- Poke around in the libraries we're using throughout this repo and try to understand how they work and what they can do. Python is great because there are sooo many libraries that help make your coding quick, easy, readable, and concise. If you're already familiar with basic logic and the logical operators, once you understand these libraries and python syntax you will be able to build whatever you can dream up. I find getting to know libraries a good way to inspire new ideas and new tools.
- If you're here trying to learn python with a penetration testing focus, try writting out all of the code instead of copy and pasting. You will make mistakes, which will force you to step through your code and understand what's working and what's not. This slower process can also help commit things to muscle memory so when you're building something new you won't have to look as much up as you've already typed things like, `self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)` so many times that it is easy to recall.
- If you're anything like me, thinking about what else you can use these tools for can really help to motivate you to keep going. Write these cool ideas down and try working off what I have here to build things more specific to your needs and curiosity.
