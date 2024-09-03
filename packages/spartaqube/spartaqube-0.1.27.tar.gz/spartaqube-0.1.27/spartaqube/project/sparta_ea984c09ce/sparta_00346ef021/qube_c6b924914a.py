_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_c8e521c5f3.sparta_d3bb2b3876 import qube_f6d3933196 as qube_f6d3933196
from project.sparta_c8e521c5f3.sparta_b71700fcc2 import qube_b0b9718cd8 as qube_b0b9718cd8
from project.sparta_c8e521c5f3.sparta_bc89190359.qube_6059f885cd import sparta_f8d86bc838
@csrf_exempt
@sparta_f8d86bc838
def sparta_96bb89c479(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_b0b9718cd8.sparta_4e540af8c3(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_f6d3933196.sparta_96bb89c479(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_f8d86bc838
def sparta_8f18df0113(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f6d3933196.sparta_a53b78f878(C,A.user);E=json.dumps(D);return HttpResponse(E)