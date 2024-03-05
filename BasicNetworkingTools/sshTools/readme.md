# SSH Tools

The tools in this directory require paramiko to be installed to run. You can either install paramiko globally  
or you can install it in a virtual environment in the project directory (sshTools) and enter the environment  
to run the tools.  
  
Creating and entering a virtual environment:  
```python3 -m venv <name of your venv> ```  
ex.  
```python3 -m venv venv3```  
Once you have created your venv, you can enter the virtual environment with:  
```source <name of vnenv>/bin/activate ```  
if you no longer want a venv you've created and wish to remove it:  
```rm -rf <venv name>```  
ex.  
```rm -rf venv3```  

### ssh_server.py

This script is set up to run on a loop back address for testing. It is also using the paramiko test_rsa.key.  
To use this script on a live deployment, you will need to generate your rsa keys and change the IP.  
  
The script is commented where you will need to change information depending on your machine/user info.  
  
Start the server on the attacker machine (usually)  
  
Generate new rsa keys:  
```ssh-keygen -t rsa -b 4096```  
name the path to save to and key name (ex./home/$USER/.ssh/'keyname'):  
enter passphrase for key:  
enter passphrase for key:  

### ssh_rcmd.py

This script is used on target machines that do not have an SSH client installed. It works in conjunction with  
ssh_server.py  
Use this script on a windows machine that doesn't have an SSH client installed.  
  
Essentially, the commands are run on the target machine running the ssh client (ssh_rcmd.py) and the output  
is sent to our server running on the attacker (ssh_server.py).  
  
### rforward.py
  
A reverse SSH port forwarding script found in the Paramiko github Demos directory.  

Just like how ssh_rcmd.py can be used from a windows machine that does not have an SSH client to connect back  
to the attacker machine running ssh_server.py, rforward.py can set up port forwarding on a windows machine  
that does not have an SSH client on it to access remote content.  
  
The remote service must be accessible to the windows target.  
  
Run this script on the windows target machine, connect it back to your attacker machine, and forward the port  
of the desired service that is only accessible to the windows target.  

### ssh_cmd.py
  
A more basic version of ssh_rcmd.py used for similar purposes.  
This script does not use key authentication, instead is uses username and password authentication.  
Use ssh_rcmd.py for use on a windows machine.  
