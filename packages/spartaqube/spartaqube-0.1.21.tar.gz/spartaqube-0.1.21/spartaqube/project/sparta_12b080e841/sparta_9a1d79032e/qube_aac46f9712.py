_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_f0e822df12():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_a3243d156d(objectToCrypt):A=objectToCrypt;C=sparta_f0e822df12();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_5f2ed00ec3(apiAuth):A=apiAuth;B=sparta_f0e822df12();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_a4fa0b959a(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_65b09e0648(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_a4fa0b959a(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_20f5ebe35e(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_a4fa0b959a(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_372871736f(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_1e88380dd7(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_372871736f(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_f443db13b6(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_372871736f(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_809f03c97a(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_56f2850909(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_809f03c97a(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_dbc3476c26(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_809f03c97a(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)