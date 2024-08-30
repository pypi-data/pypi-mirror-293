import os
from project.sparta_509f9a5b62.sparta_b9bfdd4f44.qube_c2bd03b60f import qube_c2bd03b60f
from project.sparta_509f9a5b62.sparta_b9bfdd4f44.qube_8fb7b29af3 import qube_8fb7b29af3
class db_custom_connection:
	def __init__(A):A.dbCon=None;A.dbIdManager='';A.spartAppId=''
	def setSettingsSqlite(B,dbId,dbLocalPath,dbFileNameWithExtension):G='spartApp';E=dbLocalPath;C=dbId;from bqm import settings as F,settingsLocalDesktop as H;B.dbType=0;B.spartAppId=C;A={};A['id']=C;A['ENGINE']='django.db.backends.sqlite3';A['NAME']=str(E)+'/'+str(dbFileNameWithExtension);A['USER']='';A['PASSWORD']='2change';A['HOST']='';A['PORT']='';F.DATABASES[C]=A;H.DATABASES[C]=A;D=qube_8fb7b29af3();D.setPath(E);D.setDbName(G);B.dbCon=D;B.dbIdManager=G;print(F.DATABASES)
	def getConnection(A):return A.dbCon
	def setAuthDB(A,authDB):A.dbType=authDB.dbType