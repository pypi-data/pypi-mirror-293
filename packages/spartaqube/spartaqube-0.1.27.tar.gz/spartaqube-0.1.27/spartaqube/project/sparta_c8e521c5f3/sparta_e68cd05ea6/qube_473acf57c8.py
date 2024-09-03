_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_7c01e56df3():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_2463390c62(objectToCrypt):A=objectToCrypt;C=sparta_7c01e56df3();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_5cfac83334(apiAuth):A=apiAuth;B=sparta_7c01e56df3();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_0ae2c6e1e5(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_c31d37bd27(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_0ae2c6e1e5(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_ec509e774f(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_0ae2c6e1e5(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_0525b8318f(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_7fcd4ad18c(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_0525b8318f(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_5038138190(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_0525b8318f(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_867f1c9c84(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_6e83526438(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_867f1c9c84(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_1e1ba6c9f6(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_867f1c9c84(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)