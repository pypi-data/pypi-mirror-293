import os,zipfile,pytz
UTC=pytz.utc
from django.conf import settings as conf_settings
def sparta_c8d4c551fe():
	B='APPDATA'
	if conf_settings.PLATFORMS_NFS:
		A='/var/nfs/notebooks/'
		if not os.path.exists(A):os.makedirs(A)
		return A
	if conf_settings.PLATFORM=='LOCAL_DESKTOP'or conf_settings.IS_LOCAL_PLATFORM:
		if conf_settings.PLATFORM_DEBUG=='DEBUG-CLIENT-2':return os.path.join(os.environ[B],'SpartaQuantNB/CLIENT2')
		return os.path.join(os.environ[B],'SpartaQuantNB')
	if conf_settings.PLATFORM=='LOCAL_CE':return'/app/notebooks/'
def sparta_727a352b7a(userId):A=sparta_c8d4c551fe();B=os.path.join(A,userId);return B
def sparta_1bd93e1966(notebookProjectId,userId):A=sparta_727a352b7a(userId);B=os.path.join(A,notebookProjectId);return B
def sparta_524368127a(notebookProjectId,userId):A=sparta_727a352b7a(userId);B=os.path.join(A,notebookProjectId);return os.path.exists(B)
def sparta_cad6aafbcd(notebookProjectId,userId,ipynbFileName):A=sparta_727a352b7a(userId);B=os.path.join(A,notebookProjectId);return os.path.isfile(os.path.join(B,ipynbFileName))
def sparta_e61eba3bee(notebookProjectId,userId):
	C=userId;B=notebookProjectId;D=sparta_1bd93e1966(B,C);G=sparta_727a352b7a(C);A=f"{G}/zipTmp/"
	if not os.path.exists(A):os.makedirs(A)
	H=f"{A}/{B}.zip";E=zipfile.ZipFile(H,'w',zipfile.ZIP_DEFLATED);I=len(D)+1
	for(J,M,K)in os.walk(D):
		for L in K:F=os.path.join(J,L);E.write(F,F[I:])
	return E
def sparta_77e864f912(notebookProjectId,userId):B=userId;A=notebookProjectId;sparta_e61eba3bee(A,B);C=f"{A}.zip";D=sparta_727a352b7a(B);E=f"{D}/zipTmp/{A}.zip";F=open(E,'rb');return{'zipName':C,'zipObj':F}