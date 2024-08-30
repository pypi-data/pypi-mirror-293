_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_12b080e841.sparta_83d59eaf60 import qube_1224e19839 as qube_1224e19839
from project.sparta_12b080e841.sparta_12a15bb49c import qube_3347c14f73 as qube_3347c14f73
from project.sparta_12b080e841.sparta_0687762cca.qube_90b70a692d import sparta_47f2fcf87d
@csrf_exempt
@sparta_47f2fcf87d
def sparta_97e1e195fb(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_3347c14f73.sparta_16fb16ca94(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_1224e19839.sparta_97e1e195fb(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_47f2fcf87d
def sparta_53ecb99ddd(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_1224e19839.sparta_e55c9d6024(C,A.user);E=json.dumps(D);return HttpResponse(E)