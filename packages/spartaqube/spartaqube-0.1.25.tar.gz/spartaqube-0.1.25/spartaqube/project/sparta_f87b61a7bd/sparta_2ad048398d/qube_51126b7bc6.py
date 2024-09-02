_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_40ba2b27bc.sparta_5da2ea1aa8 import qube_816b9a59f8 as qube_816b9a59f8
from project.sparta_d7b94e3744.sparta_cc6e9d39f9.qube_707ef4ff5f import sparta_4467781a0b
@csrf_exempt
def sparta_40ebc608c0(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_816b9a59f8.sparta_40ebc608c0(B)
@csrf_exempt
def sparta_b6538fdeac(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_380c6f460f(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_c30705568d(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)