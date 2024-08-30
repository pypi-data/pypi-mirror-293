_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_12b080e841.sparta_0687762cca import qube_90b70a692d as qube_90b70a692d
from project.sparta_509f9a5b62.sparta_76f284387c.qube_cb1c81c00b import sparta_8473884fda
@csrf_exempt
def sparta_37784e484f(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_90b70a692d.sparta_37784e484f(B)
@csrf_exempt
def sparta_90c43eebec(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_a3b008caef(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_d69e92b81d(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)