# GitHub Command and Control

This section is a lot of fun! We will be using GitHub as a command and control (C2) server to push code to target machines for a variety of nefarious tasks. This is a framework that you can extend by adding additional modules to add functionality to your trojans. Some chapters of this book (and sections of this repo) should give you some idea as to what you may want to add.  
  
Using GitHub as a C&C server for your trojan framework works particularly well for a few reasons:  
1. Not a lot of targets will actively block GitHub, and GitHub is what is doing the communicating.  
2. Communications between GitHub and the target will be encrypted over SSL, so your target won't be able to peak in to the network traffic.  
3. We can use a private repo so no one will be able to see what's going on (unless they hack your github account).  
  
What you'll need:  
* A github account.  
* python-github3.py. - A wrapper for the github api. Can be installed through your package manager.  
* pyinstaller to compile the trojan.
* Set up authentication on GitHub. How to can be found [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).  
 

## git_trojan.py

Check the code for notes!  
  
Things to add:  
Botnet capabilities - add the ability to automatically generate trojans, set their ID, create configuration file that's pushed to github, and compule the trojan into an executable.  
  
**class Trojan:**  
A pretty elegant object that will execute the tasks defined in the config file which is retrieved from GitHub with ```def get_config(self):``` with ```def run(self):``` which uses ```def module_runner(self, module):``` to execute, which uses ```def stored_module_result(self, data):``` to store the results of the task to an output file, and pushes the file to GitHub.  
If that sounds confusing, it's a lot easier to see what's going on by looking at the code. Read the class top to bottom, then bottom up, to see how the different class modules interact with each other. You will see that "run" -> "get_config" & "module_runner" -> "store_module_result".  

Instead of sleeping for a random period of time to avoid pattern detection (last line of ```def run(self):```), you could also generate random traffic that seems harmless to further obfuscate your pattern. Think about pulling a random number of search queries out of a premade list and generating a google search based on how many were pulled. Bonus points for adding random sleep periods between queries.  

**class GitImporter:**  
This class is used to remotely retrieve a library from our GitHub repo when it's not found on the host machine. You will need the library to be in your repo for this to work. Check the code notes for more details.  

**Still Needs to be Tested**
If you're building this in a public repo (like me), you will not want to run this trojan.  
Remember, with things like The Way Back Machine and other sleuthing techniques, once you put something on the internet, even once it's been taken down, there may still be a way for people to find it.  
If you want to play with this code, there are probably a few minor typos that you'll need to fix first. Set it up safely in a private repo and step through any traceback errors you find to fix what might be wrong.  

## Modules

Each module should expose a ```run``` function that takes a variable number of arguments so that each module can be loaded in the same way and allows you to customize the configuration files to pass different arguments to each module.  

Things to add:  
More modules to expand the capabilities of the trojan.  

* dirlister.py  
Lists all of the files in the current directory and returns them as a list.  
  
* environment.py  
Retrieves any environment variables that are set on the target machine.  

The book stops developing modules here and leaves the development of more complex modules to the reader.  

## Config

Using a configuration file allows us to to tell the trojan what actions to perform and what modules to use to perform them. This includes putting the trojan to sleep if we don't assign any tasks.  
In addition to loading the modules, a config file can also do things like set execution duration, the number of times to run the module, any arguments you want to pass to the module, and add multiple modes of exfiltrating data.  
  
To control multiple trojans and sort through the data that is retrieved, we will assign each trojan we deploy a unique ID.  

* abc.json  
A basic .json config file telling the trojan to run our 2 previously created modules.  

## Data
