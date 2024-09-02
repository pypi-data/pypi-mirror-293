_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_55934fbdfb.sparta_db8b2eb16f import qube_da95fe36a3 as qube_da95fe36a3
from project.sparta_b972c86658.sparta_741716a68d.qube_4982ec8d00 import sparta_d26395362f
@csrf_exempt
def sparta_dbac5e9c95(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_da95fe36a3.sparta_dbac5e9c95(B)
@csrf_exempt
def sparta_5e19825ca4(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_69e520b490(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_280fb8eba2(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)