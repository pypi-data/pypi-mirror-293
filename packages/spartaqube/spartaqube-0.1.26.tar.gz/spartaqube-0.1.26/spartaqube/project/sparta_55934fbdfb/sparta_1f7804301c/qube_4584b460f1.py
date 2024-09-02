_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_0592d69c2e():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_8c4f71e90c(objectToCrypt):A=objectToCrypt;C=sparta_0592d69c2e();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_9aa9bcf95b(apiAuth):A=apiAuth;B=sparta_0592d69c2e();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_18500be713(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_12ccff4d4f(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_18500be713(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_1314f0f86f(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_18500be713(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_33f0073b95(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_cdec78fff8(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_33f0073b95(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_ec376674ef(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_33f0073b95(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_4e6c0a5afe(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_f0be0f8945(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_4e6c0a5afe(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_f783b50116(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_4e6c0a5afe(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)