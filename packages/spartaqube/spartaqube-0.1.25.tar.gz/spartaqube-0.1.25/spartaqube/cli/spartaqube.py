import typer,utils as utils_cli
from pprint import pprint
from cryptography.fernet import Fernet
import spartaqube_cli as spartaqube_cli
app=typer.Typer()
@app.command()
def sparta_e715a669d4(port=None):spartaqube_cli.runserver(port)
@app.command()
def list():spartaqube_cli.list()
@app.command()
def sparta_b3714494fe():spartaqube_cli.sparta_b3714494fe()
@app.command()
def sparta_4603228f4a(ip_addr,http_domain):A=spartaqube_cli.token(ip_addr,http_domain);print(A)
@app.command()
def sparta_14ead057f0():print('Hello world!')
if __name__=='__main__':app()