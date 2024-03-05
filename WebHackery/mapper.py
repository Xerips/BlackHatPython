import contextlib
import os
import queue
import requests
import sys
import threading
import time

FILTERED = [".jpg", ".gif", ".png", ".css"] # We AREN'T interested in these files. Filter out.
TARGET = "http://boodelyboo.com/wordpress" # Replace with your target website.
THREADS = 10 # Change number of threads according to your needs.

answers = queue.Queue() # Queue object where we "put" the file paths we've located locally.
web_paths = queue.Queue() # Second Queue object where we'll store the files we'll attempt to locate on remote server.

def gather_paths():
    for root, _, files in os.walk('.'): # os.walk to walk through the local web application directory.
        for fname in files:
            if os.path.splitext(fname)[1] in FILTERED:
                continue
            path = os.path.join(root, fname)
            if path.startswith('.'):
                path = path[1:]
            print(path)
            web_paths.put(path)

@contextlib.contextmanager
def chdir(path):
    """
    On enter, change directory to specified path.
    On exit, change directory back to original.
    """
    this_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(this_dir)

def test_remote(): # Tests your local install of WP against the remote target's file system for matches.
    while not web_paths.empty():
        path = web_paths.get()
        url = f'{TARGET}{path}'
        time.sleep(2) # Your target may have throttling/lockout. Increase as needed.
        r = requests.get(url)
        if r.status_code == 200:
            answers.put(url)
            sys.stdout.write('+')
        else:
            sys.stdout.write('x')
        sys.stdout.flush()

def run():
    mythreads = list()
    for i in range(THREADS):
        print(f'Spawning thread {i}')
        t = threading.Thread(target=test_remote)
        mythreads.append(t)
        t.start()

    for thread in mythreads:
        thread.join()

if __name__ == "__main__":
    with chdir("/home/$USER/Work/wordpress/wordpress-install"): # Change to your local WP install.
        gather_paths()
    input('Press return to continue.') # Chance to review before executing on target.

    run()
    with open('myanswers.txt', 'w') as f:
        while not answers.empty():
            f.write(f'{answers.get()}\n')
    print('done')
