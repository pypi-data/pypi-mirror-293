_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_8910388a9c():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_050f894f0e(objectToCrypt):A=objectToCrypt;C=sparta_8910388a9c();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_7363b6f35a(apiAuth):A=apiAuth;B=sparta_8910388a9c();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_4ef57de5fc(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_f0cddb53a0(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_4ef57de5fc(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_0d2eeacc52(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_4ef57de5fc(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_6999b521c4(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_317cb34406(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_6999b521c4(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_0dc4e2555c(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_6999b521c4(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_692d56fea9(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_cfda5885f8(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_692d56fea9(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_a6e23635a1(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_692d56fea9(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)