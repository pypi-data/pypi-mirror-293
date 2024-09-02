_A='jsonData'
import json,inspect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from project.sparta_55934fbdfb.sparta_50ad56a15b import qube_f0edb997d4 as qube_f0edb997d4
from project.sparta_55934fbdfb.sparta_db8b2eb16f.qube_da95fe36a3 import sparta_2dd23776f5
@csrf_exempt
@sparta_2dd23776f5
def sparta_06a948083b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f0edb997d4.sparta_06a948083b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2dd23776f5
def sparta_b3ba731330(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_f0edb997d4.sparta_b3ba731330(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_2dd23776f5
def sparta_c7c7bd2061(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_f0edb997d4.sparta_c7c7bd2061(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_2dd23776f5
def sparta_c83f7bcd61(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f0edb997d4.sparta_c83f7bcd61(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2dd23776f5
def sparta_1a0a332874(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f0edb997d4.sparta_1a0a332874(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2dd23776f5
def sparta_b3eb3e9e55(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f0edb997d4.sparta_b3eb3e9e55(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_461fdb6fd8(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_f0edb997d4.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_2dd23776f5
def sparta_ee06f7ebeb(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f0edb997d4.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_42559aa209(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_f0edb997d4.sparta_42559aa209(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_120f3c8dcf(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f0edb997d4.sparta_120f3c8dcf(A,C);E=json.dumps(D);return HttpResponse(E)