_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_55934fbdfb.sparta_566a6d0688 import qube_f76c13c2cd as qube_f76c13c2cd
from project.sparta_55934fbdfb.sparta_2c7485b6ab import qube_0f88a22cae as qube_0f88a22cae
from project.sparta_55934fbdfb.sparta_db8b2eb16f.qube_da95fe36a3 import sparta_2dd23776f5
@csrf_exempt
@sparta_2dd23776f5
def sparta_8113460523(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_0f88a22cae.sparta_64510e0deb(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_f76c13c2cd.sparta_8113460523(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_2dd23776f5
def sparta_0461234939(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f76c13c2cd.sparta_3c3f55f6d6(C,A.user);E=json.dumps(D);return HttpResponse(E)