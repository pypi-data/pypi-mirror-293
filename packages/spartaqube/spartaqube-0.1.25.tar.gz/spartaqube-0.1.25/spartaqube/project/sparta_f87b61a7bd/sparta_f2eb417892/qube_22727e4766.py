_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_40ba2b27bc.sparta_d8dc063cad import qube_b5892842c0 as qube_b5892842c0
from project.sparta_40ba2b27bc.sparta_f1aa1afeb1 import qube_de9a3677f3 as qube_de9a3677f3
from project.sparta_40ba2b27bc.sparta_5da2ea1aa8.qube_816b9a59f8 import sparta_59f81fc832
@csrf_exempt
@sparta_59f81fc832
def sparta_8448f9aef0(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_de9a3677f3.sparta_35ed92202f(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_b5892842c0.sparta_8448f9aef0(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_59f81fc832
def sparta_b3f67a5a41(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_b5892842c0.sparta_feefb8caf5(C,A.user);E=json.dumps(D);return HttpResponse(E)