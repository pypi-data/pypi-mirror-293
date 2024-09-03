import typer,utils as utils_cli
from pprint import pprint
from cryptography.fernet import Fernet
import spartaqube_cli as spartaqube_cli
app=typer.Typer()
@app.command()
def sparta_05483b5c2f(port=None):spartaqube_cli.runserver(port)
@app.command()
def list():spartaqube_cli.list()
@app.command()
def sparta_66d923321c():spartaqube_cli.sparta_66d923321c()
@app.command()
def sparta_6e7988d4b5(ip_addr,http_domain):A=spartaqube_cli.token(ip_addr,http_domain);print(A)
@app.command()
def sparta_31f0b4a627():print('Hello world!')
if __name__=='__main__':app()