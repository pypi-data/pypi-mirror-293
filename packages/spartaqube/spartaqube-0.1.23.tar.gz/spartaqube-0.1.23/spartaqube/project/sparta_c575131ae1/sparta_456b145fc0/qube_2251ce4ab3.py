_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_30e2c8fafc.sparta_33b80ccaf4 import qube_b645503fa4 as qube_b645503fa4
from project.sparta_30e2c8fafc.sparta_dc1e3836d5 import qube_b1cef934b3 as qube_b1cef934b3
from project.sparta_30e2c8fafc.sparta_4f7fa902d8.qube_b0ccd99581 import sparta_25b99b49dd
@csrf_exempt
@sparta_25b99b49dd
def sparta_b26f490c3a(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_b1cef934b3.sparta_220edd9863(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_b645503fa4.sparta_b26f490c3a(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_25b99b49dd
def sparta_0c824d1b50(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b645503fa4.sparta_f793e456ac(C,A.user);E=json.dumps(D);return HttpResponse(E)