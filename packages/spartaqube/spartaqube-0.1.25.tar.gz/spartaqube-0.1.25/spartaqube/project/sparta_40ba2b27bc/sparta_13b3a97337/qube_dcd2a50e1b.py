import os,zipfile,pytz
UTC=pytz.utc
from django.conf import settings as conf_settings
def sparta_de39e17a7d():
	B='APPDATA'
	if conf_settings.PLATFORMS_NFS:
		A='/var/nfs/notebooks/'
		if not os.path.exists(A):os.makedirs(A)
		return A
	if conf_settings.PLATFORM=='LOCAL_DESKTOP'or conf_settings.IS_LOCAL_PLATFORM:
		if conf_settings.PLATFORM_DEBUG=='DEBUG-CLIENT-2':return os.path.join(os.environ[B],'SpartaQuantNB/CLIENT2')
		return os.path.join(os.environ[B],'SpartaQuantNB')
	if conf_settings.PLATFORM=='LOCAL_CE':return'/app/notebooks/'
def sparta_1c4e940d04(userId):A=sparta_de39e17a7d();B=os.path.join(A,userId);return B
def sparta_dd19bd1a87(notebookProjectId,userId):A=sparta_1c4e940d04(userId);B=os.path.join(A,notebookProjectId);return B
def sparta_bb5adc91a3(notebookProjectId,userId):A=sparta_1c4e940d04(userId);B=os.path.join(A,notebookProjectId);return os.path.exists(B)
def sparta_b191432ca1(notebookProjectId,userId,ipynbFileName):A=sparta_1c4e940d04(userId);B=os.path.join(A,notebookProjectId);return os.path.isfile(os.path.join(B,ipynbFileName))
def sparta_0b78dd98f9(notebookProjectId,userId):
	C=userId;B=notebookProjectId;D=sparta_dd19bd1a87(B,C);G=sparta_1c4e940d04(C);A=f"{G}/zipTmp/"
	if not os.path.exists(A):os.makedirs(A)
	H=f"{A}/{B}.zip";E=zipfile.ZipFile(H,'w',zipfile.ZIP_DEFLATED);I=len(D)+1
	for(J,M,K)in os.walk(D):
		for L in K:F=os.path.join(J,L);E.write(F,F[I:])
	return E
def sparta_d05a09ac44(notebookProjectId,userId):B=userId;A=notebookProjectId;sparta_0b78dd98f9(A,B);C=f"{A}.zip";D=sparta_1c4e940d04(B);E=f"{D}/zipTmp/{A}.zip";F=open(E,'rb');return{'zipName':C,'zipObj':F}