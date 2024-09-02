import typer,utils as utils_cli
from pprint import pprint
from cryptography.fernet import Fernet
import spartaqube_cli as spartaqube_cli
app=typer.Typer()
@app.command()
def sparta_7d6ad79814(port=None):spartaqube_cli.runserver(port)
@app.command()
def list():spartaqube_cli.list()
@app.command()
def sparta_6d74ffc561():spartaqube_cli.sparta_6d74ffc561()
@app.command()
def sparta_0a08772529(ip_addr,http_domain):A=spartaqube_cli.token(ip_addr,http_domain);print(A)
@app.command()
def sparta_ee5a4ea394():print('Hello world!')
if __name__=='__main__':app()