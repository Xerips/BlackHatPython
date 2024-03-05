import queue
import requests
import threading
import sys

AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0" # We're regular users, promise!
EXTENSIONS = ['.php', '.bak', '.orig', '.inc', '.zip', '.pdf', '.config', '.txt'] # Add more, find more.
TARGET = "http://testphp.vulnweb.com" # Change to whatever Target you're testing.
THREADS = 50
WORDLIST = "/usr/share/seclists/Discovery/Web-Content/SVNDigger/all.txt" # Location of wordlist you want to use.

def get_words(resume=None):

    def extend_words(word): # Inner function because extend_words will always be used with get_words.
        if "." in word:
            words.put(f'/{word}') # Brute forcing files.
        else:
            words.put(f'/{word}/') # Brute forcing directories.

        for extension in EXTENSIONS:
            words.put(f'/{word}{extension}')

    with open(WORDLIST) as f:
        raw_words = f.read() # Read in the wordlist you've specified.

    found_resume = False
    words = queue.Queue()
    for word in raw_words.split():
        if resume is not None: # Allows to resume the brute force if it's interrupted.
            if found_resume:
                extend_words(word)
            elif word == resume:
                found_resume = True
                print(f'Resuming wordlist from: {resume}')
        else:
            print(word)
            extend_words(word)
    return words # Return a Queue of words from the wordlist to brute force with.

def dir_bruter(words):
    headers = {'User-Agent': AGENT}
    while not words.empty():
        url = f'{TARGET}{words.get()}'
        try:
            r = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError:
            sys.stderr.write('x');sys.stderr.flush()
            continue

        if r.status_code == 200:
            print(f'\nSuccess ({r.status_code}: {url})')
        elif r.status_code == 404:
            sys.stderr.write('.');sys.stderr.flush()
        else:
            print(f'{r.status_code} => {url}')

if __name__ == "__main__":
    words = get_words()
    print('Press return to continue.')
    sys.stdin.readline()
    for _ in range(THREADS):
        t = threading.Thread(target=dir_bruter, args=(words,))
        t.start()
