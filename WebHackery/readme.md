# Web Hackery

The beginning of this chapter of the book goes over some of the libraries you will need in dealing with web servers. These include:  
* urllib - Don't. Just don't. Unless you have to. You may need to write a tool to work on a system that doesn't have requests installed and you cannot or don't want to (noise) install it.  
* requests - Do. Just do. Unless you can't.  
* lxml - Helps parse the contents of HTTP responses. Can use instead of or with BeautifulSoup.  
* beautifulsoup4 - Helps parse the contents of HTTP responses. Can be used instead of or with lxml.  
  
A few tools that merrit getting familiar with that operate within the same vein as many of these tools:  

* curl - Make web requests from the terminal (a simple yet robust HTTP tool).  
* httpie - A more user friendly HTTP tool.  
* hydra - Great tool for bruteforcing passwords and/or usernames over many different protocols.  
* burpsuite - In addition to being a proxy, you can use burp for cluster bomb attacks, fork attacks, and much more to brute force passwords/usernames from lists.
* gobuster - Directory busting tool of choice (could also see dirbuster, dirb, ffuf, dirsearch). Sometimes one list or tool will work where another one won't.  
* wfuzz - A fuzzer that can be used to fuzz different parameters to do a multitude of cool things (also see fuff).  
* WPScan - Pen testing Word Press sites.  
* Jaidam - Pen testing with both WPScan and Joomscan.  

### bruter.py

**Description:**  
A tool used to brute force web directories and files.  
  
The book suggests and uses [SVNDigger](https://www.invicti.com/blog/web-security/svn-digger-better-lists-for-forced-browsing/) and [gobuster](https://github.com/OJ/gobuster)'s wordlists. For the creme de la creme of wordlists, try out Seclists. Seclists contains both of the recommendations from the book and can be installed through most package managers, or directly from Daniel Miessler's [github](https://github.com/danielmiessler/SecLists).  
The added benefit of installing seclists through your package manager, is that it will update when you update your installed packages.  
  
* I've added a few extra file extensions in EXTENSIONS = []. I will often play with including different file extensions when I'm working on a box to see if I can dredge up anything extra. Do the same, play around!  
* This tool will iterate on top of found files. For example, you may find admin.php. The tool will also look for admin.php.bak, admin.php.orig, etc.  

* If you only want to print out the successes, you can filter out errors (send errors to /dev/null) just run the tool with 2> /dev/null.  
``` python3 bruter.py 2> /dev/null```  
* Using 2> /dev/null is a powerful addition to many terminal commands you might run such as ```find / -user root -perm /4000 2>/dev/null```.  

### wordpress-killer

**Description:**  
A tool used to bruteforce wordpress login pages.  
  
* This tool will automatically detect the username, password, and cookie parameters to use while brute forcing. It does this by parsing the html of the login page you're attempting to brute force. To look up these parameters manually, view-source on the login page by right clicking, or prepending "view-source:" to the url:  
```view-source:https://<your-target>/wp-login.php```  
* Wordpress requires you to submit your session cookie with the login attempt or even with valid credentials, the login attempt will fail. We will handle cookies automatically with the requests library's Session object.  
  
* The request flow is the following:  
1. Retrieve the login page and accept all cookies that are returned.  
2. Parse out all of the form elements from the HTML.  
3. Set the username and/or password to a guess from our dictionary.  
4. Send an HTTP POST to the login processing script, including all HTML form fields and our stored cookies.  
5. Test to see if we have successfully logged in to the web application.  

* This tool doesn't work right out of the book. You must remove the very last ) from the code in the book, it's a misprint. To avoid the "url not defined" error you get from following the book, change the 2nd last line from: ```b = Bruter('tim', url)``` to: ```b = Bruter('tim', TARGET)```. This has been changed in the code I uploaded, but might be your issue if you're here looking for help getting this tool to work.  
* There are multiple comments in the code to help understand how it works.  
* If you end up using this tool for bruteforcing wordpress, you may want to comment out ```print(f'Trying username/password {self.username}/{passwd:<10}')``` on line 55. It will tell you that the tool is still working (a plus), but it can get annoying.  

### mapper.py

This tool requires a local installation of WordPress. You can Download the zip file [here](https://wordpress.org/download/). Unzip the file wherever is convenient for you, and add the location to mapper.py where it's commented to do so.  

**Description:**  
This tool leverages a local installation of WP (installed on your/host machine), to compare that directory hierarchy and files with a remote host and save the results to a file which contains a map of the WordPress (WP) target site.  
  
I think the most valuable part of this tool is learning how to use contextmanager to ensure your script is working in the right directory. The book even suggests to save the chdir function in your utilities to be able to use it in other scripts.  

*Some notes found in the mapper.py code.  
  
def chdir(path):  
* chdir uses a context manager to simplify the use of the tool. Context manager are useful when you've opened something and need to close it, locked something and need to release it, or changed something and need to reset it.  
* You generally create a context manager by creating a class with the ```__enter__``` and ```__exit__``` methods. ```__enter__``` returns the resouce that needs to be managed (a file, socket, etc.) and the ```__exit__``` method performs the cleanup (closing, resetting, etc).  
* We don't need that much control here, and so we use the @contextlib.contextmanager to create a simple context manager that converts a generator function into a context manager.  
* chdir function enables you to executre code inside a different directory and guarantees that, when you exit, you'll be returned to the original directory.  
* chdir generator function initializes the context by saving the original directory and changing into a new one, yields control back to gather_paths, and then reverts to the original directory.  
* We use the "try/finally" block here instead of "try/except." Unlike except, finally will always execute, regardless of errors. This is obviously quite powerful if you're likely to break things and want to revert back to the original files "no matter what."  
* The book provides a nice little code block to show the difference between "try/except" and "try/finally.":  
```
try:
    something_that_might_cause_an_error()
except SomeError as e:
    print(e)                # Show the error on the console.
    Dosomethingelse()       # Take some alternative action.
else:
    everything_is_fine()    # This executes only if the try succeeded.
finally:
    cleanup()               # This executes no matter what.
```

### basic_request.py

Very basic request script showcasing requests library.  

### bs_link_parse.py & lx_link_parse.py

Running these scripts will print out all of the links on the web page you specify along with their hyperlink text.  
/<some info her> indicates a link that is part of the website. For this example the last line printed "/privacypolicy.htm" belongs to nostarch.com and is located at http://nostarch.com/privacypolicy.htm.  

### urllib_scripts/:

#### GET_request.py & POST_request.py

These tools use urllib to make GET and POST requests which is a standard python library for interacting with web servers. Urllib contains the following modules that you can import into your script to access it's functionality:  
urllib.request  
urllib.error  
urllib.parse  
urllib.robotparser  
  
You might be thinking, "Hey, urllib sucks, use requests instead!" To which we, the authors, and python3, answer, "Okay!"  
However, you could be working from a compromised machine that only has bare bones python3 or python2 (get with the times people!), in which case you may not be able to install requests and so only urllib will be accessible to you.  
  
* If you ever find yourself on a target system which has wildly out of date software on it, you should be looking at what software is vulnerable to priv. esc. exploits. Once you get root, it doesn't really matter what was there before (for the most part).  
