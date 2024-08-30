import typer,utils as utils_cli
from pprint import pprint
from cryptography.fernet import Fernet
import spartaqube_cli as spartaqube_cli
app=typer.Typer()
@app.command()
def sparta_c9d9d1f418(port=None):spartaqube_cli.runserver(port)
@app.command()
def list():spartaqube_cli.list()
@app.command()
def sparta_23fd3e8989():spartaqube_cli.sparta_23fd3e8989()
@app.command()
def sparta_0999dcb51a(ip_addr,http_domain):A=spartaqube_cli.token(ip_addr,http_domain);print(A)
@app.command()
def sparta_7cb9a42e6a():print('Hello world!')
if __name__=='__main__':app()