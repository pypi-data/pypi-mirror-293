_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_342f8baa54():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_a7892502ac(objectToCrypt):A=objectToCrypt;C=sparta_342f8baa54();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_9a926fc6f8(apiAuth):A=apiAuth;B=sparta_342f8baa54();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_cd5424e300(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_f43a15b562(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_cd5424e300(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_e195d0f81f(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_cd5424e300(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_c0ecf08f39(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_5af64926db(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_c0ecf08f39(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_409ffd2e89(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_c0ecf08f39(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_a811a74938(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_fa51d2f615(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_a811a74938(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_6ff9767646(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_a811a74938(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)