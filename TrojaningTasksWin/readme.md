# Trojaning Tasks for Windows

Black Hate Python only contains a section on trojaning tasks for windows, not for linux. This is because linux users are never deserving of being targetted by malicious actors. Or it's because the vast majority of personal computers use windows and if you're trying to infect a bunch of computers to form a bot net or priv esc into something more juicy, you're likely to have more success targetting a bunch of personal computers (this includes computers used by businesses for employees usage). Either way, that's all you get. However, if you're familiar with linux, using shell commands in conjunction with you script would be an easy way to expand the functionality to linux.  

### keylogger.py

You'll need:  
* [PyWinHook](https://pypi.org/project/pyWinhook/)  
* A windows machine or virtual machine to test the module.

keylogger.py uses the PyWinHook library to take advantage of the Windows function SetWindowsHookEx. This allows us to install a user-defined function to be called for certain Windows events - like keyboard events. We will also want to know what process the keystrokes are being used with so we can better determine if the keystrokes are usernames or passwords.  
  
You will notice that this module uses ```def run():``` which allows us to load and run the module just like the other modules we have in the GitHubTrojan directory.  
  
See the code for comments.  

### screenshotter.py

You'll need:  
* pywin32  
  
In this module, we create a device context. Learn more about device context and GDI programming [here](http://msdn.microsoft.com).  

See code for notes.  

### shell_exec.py

Notes:  
In order to execute raw shellcode without teouching the filesystem, we need to create a buffer in memory to hold the shellcode and, using the ctypes module, create a function pointer to that memory.  
To do this, we call the function and use urllib to grab the shellcode from a web server in base64 format and execute it.  
We use VirtualAlloc to allocate the memory we need to store the code in the buffer, and RtlMoveMemory to move the buffer containing the shellcode into the allocated memory.  
We must specify that the result we want back from VirtualAlloc is a pointer (ptr), and the arguments will be 2 pointers and a size object. Without this the width of the memory address returned from VirtualAlloc will not match the width that RtlMoveMemory expects.  
0x40 specifies that the memory should have read, write, execute permissions.  

Remember, the internal IP you use when working on hackthebox or vulnhub is just that, internal. When you vpn into these services or spin up a virtual machine you're on the same network. To serve shellcode to a remote machine (not connected to your network), you will need to use your public IP address. This is most likely an IPv6 address unless you've registered a domain. Consider using a filesharing website or build your own server on something like linode/akamai. You could also use your GitHub.  

See code for notes.  

### sandbox_detect.py

This module helps us to determine whether our Trojan is operating within a sandbox. The easiest way to see the difference between a sandbox and a real machine is through inspecting the user input. A sandbox will have no user input, as they only run automatied malware analysis. A real machine will have multiple mouse clicks, keystrokes, etc. to indicate someone is using the machine.  
A sandbox may have varying degrees of anti-sandbox detection techniques, like random inputs. This module will try to detect the most rudimentary version of this.  
  
It's interesting to note that not just attackers need to think like a hacker, blue teamers should also try to obfuscate their detection techniques. It's not just the black hats that should try to be sneaky and clever.  
  
There are many reasons to tweak the values of this module. Primarily, your values will be determined by how the target was infected. Did you use some sort of phishing technique to get the user to download the trojan? If so, you'd expect to see input almost immediately after infection as you would have to have an active user on the machine for this infection type to happen. If you've uploaded the trojan yourself through some sort of vulnerability, there may not be any active users on the system (depending on what it is), and so it may take more time to register some user input.  

See code for notes.  
