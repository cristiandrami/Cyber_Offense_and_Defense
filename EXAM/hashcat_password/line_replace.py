



import typer

from lxml import html
from rich.console import Console
from rich.progress import track

console = Console()
app = typer.Typer()


@app.command()
def run(input_file:str, output_file:str):
    lines_to_replace = 1500
    modified_lines =[] 
    with open(input_file, 'r', encoding='latin-1') as file:
        for indx, line in enumerate(file):
            if indx > lines_to_replace:
                break
            modified_lines.append("COD{"+line.strip()+"}\n")

    with open(output_file, 'w') as file:
        file.writelines(modified_lines)
     

    

if __name__ == "__main__":
    app()