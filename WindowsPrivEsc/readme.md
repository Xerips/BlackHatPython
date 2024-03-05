# Windows Privilege Escallation

This section uses a few different tools to create a reliable way to endeavor to escallate privileges on a windows target via code injection.  

### bhservice.py

A basic service you can install and run on a windows victim for testing or as a skeleton to start building malware. To test features like the code injection found in file_monitor.py, you can run this service wait for it to start outputting files, then see if file_monitor.py can catch the files and write to them before the files are executed and erased by the script.  
If you can install this on a victim machine, it could also provide an entry point for code injection.
  
If you want to create a real service on a victim machine, this skeleton gives you the outline for how to structure one. Find the ```bhservice_tasks.vbs``` script [here](https://nostarch.com/black-hat-python2E/). Place the file in a directory with bhservice.py and change the SRCDIR to point to this directory.  
  
To turn your script into an executable, you can use pyinstaller:  
```pyinstaller -F --hiddenimport win32timezone bhservice.py```  
This tool is also useful for the trojan section of the project. You can turn your trojan into an executable the same way.  
Once your script has been saved as a .exe, you can install and start it on the victim machine with:  
```bhservice.exe install```  
```bhservice.exe start```  
Every minute, the service will write the script file into a temp dir, execute the script, and delete the file.  
  
To stop the service:  
```bhservice.exe stop```  
To remove the service when you're done experimenting:  
```bhservice.exe remove```  
To update the service, skip the install step and replace it with:  
```bhservice.exe update```  
  
For any changes to the bhservice.py script, you will have to convert the new script to an .exe, update, and starting the service.  
  
Required installed libraries:  
pywin32  
pyinstaller  
wmi (for process_monitor.py)  

On windows install these libraries with:  
```C:\Users\foo\work> pip install pywin32 wmi pyinstaller```  

### process_monitor.py

In this section the authors point out some valuable tid bits about antivirus detection. The biggest take away is that using a system monitor offensively to gather intel on potential victims through hooking ```CreateProcess``` calls can be problematic. This is because anti-virus software also hook the ```CreateProcess``` function and doing so could get you labelled as malware or at the vary least lead to instability issues. This tool is therefore designed to be hookless to avoid these issues.  

Although the tool is designed for offensive purposes, it is also a good tool for defensive purposes. By running this tool and seeing what processes being run, you may be able to detect malware if it's present on the host machine.  

The Windows Management Instrumentation (WMI) API allows us to monitor a system for certain events, and to receive callbacks when those events occur.  
What we get from this tool:  
* Receive a callback every time a new process is created.  
* Prints to screen and Logs to file:  
    * Time the process was created.  
    * User who spawned the process.  
    * The executable that was launched and its cli arguments.  
    * The process ID.  
    * The parent process ID.  
    * Determines privileges of the process tokens.  

This tool needs to be run as administrator in order to capture information about high-privilege processed created by SYSTEM.  
This tool was adapted from the [Python WMI page](http://timgolden.me.uk/python/wmi/tutorial.html).  
Lookup MSDN Documentation online for more information on the Win32_Process WMI class.  
If you cannot load these modules, you can translate them from the functions in the script to native calls using the ctypes library. It's a lot more work, and isn't covered here.  

**How to use:**  

* Run the script for long enough to gather a good amount of info on what processes the users and machine are running (a day, a week, etc.). You will see records showing all the running processes, scheduled tasks, and updaters. You may even see some malware if it already exists on the system. Logging out then in again with the script running can also help to generate some useful information.  
* Just because you can't run the script as Administrator or SYSTEM, does not mean it's game over. Keep an eye out for processes that have weird permissions that might indicate misconfiguration. A process running as a user with the wrong privileges is an easy way to get to SYSTEM or run code in the kernel.  

**Privileges to look out for:**  

| Privilege Name | Access that is granted |
|----------------|------------------------|
| SeBackupPrivilege | This enables the user process to back up file and directories, and it grants READ access to files no matter what their access control list (ACL) defines. |
| SeDebugPrivilege | This enables the user process tod ebug other processes. It also includes obtaining process handles to inject DLLs or code into running processes. |
| SeLoadDriver | This enables a user process to laod or unload drivers. |
  
**Windows Token Privileges:**  

A windows token is, "an object that describes the security context of a process or thread." The token's permissions and privileges determine which tasks a process or thread can perform.  
An app that uses the native Windows API function ```AdjustTokenPrivileges``` to achieve some sort of functionality would grant the app the SeLoadDriver privilege. Now, if an attacker is able to get control over the application, they could protentially load or unload any driver they want. Dropping a kernel mode rootkit at this point would be trivial.  

### file_monitor.py

This is a spiffy little tool. It will do two things:  
1. Monitor a given directory or directories, to see if a file has been created, deleted, modified, renamed from, or renamed to. It will print these modifications to the terminal.  
    * While an enterprise system is running, you will often find PowerShell, Batch, and VBScript scripts performing automated tasks.  
    * With the process_monitor.py tool, you may see that these scripts are doing things like spawning the ```wscript.exe``` binary and passed in the ```C:\WINDOWS\TEMP\bhservice_task.vbs``` parameter. But when you look at the directory, you don't see this file present.  
    * This is because our script, and many other scripts used for automating tasks, will create a file containing VBScript, execute the script, then remove the file containing the VBScript. This is most commonly done in the temp directory.  
2. Perform a Code Injection by "winning the race" between when the file is created, the code is executed, and the file is removed.  
    * We essentially need to be able to inject our code into the file before the process executes and deletes it.  
    * In the current state, file_monitor.py will inject code that starts a nc listener on the machine for us to be able to connect to.  

If you haven't created an executable of the NetCat.py we created earlier, do so here to be able to use code injection.  
```pyinstaller -F netcat.py```  

How useful would it be to implement this with our trojan to establish a backdoor, or expand on our functionality through code injection...?  
