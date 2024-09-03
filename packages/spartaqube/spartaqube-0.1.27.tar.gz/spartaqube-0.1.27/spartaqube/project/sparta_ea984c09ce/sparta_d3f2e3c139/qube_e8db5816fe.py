_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_c8e521c5f3.sparta_bc89190359 import qube_6059f885cd as qube_6059f885cd
from project.sparta_3ca0064d9b.sparta_e277eee10c.qube_b6b724ff27 import sparta_f29a5d8d9b
@csrf_exempt
def sparta_5a1cd67310(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_6059f885cd.sparta_5a1cd67310(B)
@csrf_exempt
def sparta_c3e94e0f78(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_86f51a62cd(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_607f99facd(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)