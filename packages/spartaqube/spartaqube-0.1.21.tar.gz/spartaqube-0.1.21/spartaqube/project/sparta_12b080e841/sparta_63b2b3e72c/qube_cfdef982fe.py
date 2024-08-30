import re,os,json,requests
from datetime import datetime
from project.models import AppVersioning
import pytz
UTC=pytz.utc
def sparta_07859de04d():0
def sparta_2736849e1a():
	try:A='https://pypi.org/project/spartaqube/';B=requests.get(A).text;C=re.search('<h1 class="package-header__name">(.*?)</h1>',B,re.DOTALL);D=C.group(1);E=D.strip().split('spartaqube ')[1];return E
	except:pass
def sparta_47ae433e19():
	B=os.path.dirname(__file__);C=os.path.dirname(B);D=os.path.dirname(C);E=os.path.dirname(D)
	try:
		with open(os.path.join(E,'app_version.json'),'r')as F:G=json.load(F);A=G['version']
	except:A='0.1.1'
	return A
def sparta_63acf88f97():
	F='res'
	try:
		C=sparta_47ae433e19();A=sparta_2736849e1a();D=AppVersioning.objects.all();E=datetime.now().astimezone(UTC)
		if D.count()==0:AppVersioning.objects.create(last_available_version_pip=A,last_check_date=E)
		else:B=D[0];B.last_available_version_pip=A;B.last_check_date=E;B.save()
		return{'current_version':C,'latest_version':A,'b_update':not C==A,'humanDate':'A moment ago',F:1}
	except Exception as G:return{F:-1,'errorMsg':str(G)}