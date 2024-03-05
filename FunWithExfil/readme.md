# Fun with Exfiltration

### exfil.py

The main tool which uses the modules detailed below to perform exfiltration.  
  
Because this is designed to use with a trojan, you need to pre determine the exfil type in the last line of the code (see comments in code). Alternatively, you could write some additional code to iterate through methods and check for success of exfiltration, to allow your trojan to try multiple methods and determine when to stop (on success). This isn't covered in the book, but would definitely be possible with what we've learned.  
  
Note: the EXFIL dictionary makes things easy because in Python, functions are first class citizens and can be used as parameters. This technique is sometimes called *dictionary dispatch*.  

## modules

### cryptor.py

You'll need:  
* PyWin32  
* pycryptodomex  
  
Extra Notes:  
* We will use both symmetric and asymmetric encryption to get the best of both worlds.  
    * AES cipher for symmetric encryption. - symmetric because it uses the same key for encryption and decryption.  
    * RSA for asymmetric encryption. - asymmetric because it a 2 key pair, public and private key.  

### email_exfil.py

You will use crypto.py to first encrypt the files, then send using email_exil.py.  
After using email_exfil.py to send an encrypted file to your host/attacker machine, you'll need to copy the contents of the email to a new file then read that file into cryptor.py in order to decrypt it.  


### transmit_exfil.py

You will use cryptor.py to first encrypt the files, then send using transmit_exfil.py.  
After using transmit_exfil.py to send an encrypted file to your host/attacker machine, you'll use cryptor.py to decrypt the contents.  

### paste_exfil.py

In this method, we have hardcoded the username and password to a ficticious Pastbin account. This is not best practice for obvious reasons. If you're going to use this in its current state, you'll want to use an account that has some added opsec.  
I have added a small readme on opsec in the /BHP main directory.  
  
Automates the process of posting the encrypted document to a pastebin.com account. Pastebin is also widely used, so it gives us a better chance of avoiding blacklisting from a firewall or proxy.  

You will have to login to your account and download the paste from your dashboard in order to decrypt using cryptor.py.  

#### Windows Specific paste_exfil.py 

There are lots of articles online to help you better understand the Document Object Model (DOM). As we're interacting with it here, it would be good to brush up on what it is and how it works.  

Internet Explorer COM automation has the benefit of using Iexplore.exe, which is typically trusted and whitelisted, to exfiltrate information out of a network. It is important to note that IE has been deprecated by windows and is less likely to be present on newer systems.  

The authors state that they had to manually inspect the UI elements for pastebin by inspecting each HTML element that needs to be interacted with. If you want to use a different service than pastebin, you will need to figure out the precise timing, DOM interactions, and HTML elements that are required for that different service.  

### Bonus Tools:

#### decryptor.py

I don't particularly like creating a new script for every file we receive and want to decrypt. So, I've made this little tool that will take the file path as a user input and decrypt the file we've exfiltrated.  

#### dir_decryptor.py

Don't want to run the script multiple times for every file you've got sitting waiting to be decrypted. I got you covered! This tool really shows the power of python, with one method, one standard library, and just over 20 lines of code (minus blank lines and comments), we can automate the process of decrypting multiple files and writing them to a new directory.  

#### dirty_decrypt.py

The book provides a quick and dirty script to decrypt a file using our cryptor.py method. You will find this under dirty_decrypt.py if you prefer to play with things that way.  
