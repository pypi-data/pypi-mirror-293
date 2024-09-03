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
from project.sparta_c8e521c5f3.sparta_c50af81fe6 import qube_711627e27b as qube_711627e27b
from project.sparta_c8e521c5f3.sparta_bc89190359.qube_6059f885cd import sparta_f8d86bc838
@csrf_exempt
@sparta_f8d86bc838
def sparta_afe54917c8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_711627e27b.sparta_afe54917c8(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f8d86bc838
def sparta_e878a40845(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_711627e27b.sparta_e878a40845(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_f8d86bc838
def sparta_4b149dfb11(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_711627e27b.sparta_4b149dfb11(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_f8d86bc838
def sparta_9278876cbe(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_711627e27b.sparta_9278876cbe(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f8d86bc838
def sparta_2ed7c40b6b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_711627e27b.sparta_2ed7c40b6b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f8d86bc838
def sparta_883e41324d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_711627e27b.sparta_883e41324d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_9a94913712(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_711627e27b.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_f8d86bc838
def sparta_0c39c511a6(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_711627e27b.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_904a937745(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_711627e27b.sparta_904a937745(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_59cca6f436(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_711627e27b.sparta_59cca6f436(A,C);E=json.dumps(D);return HttpResponse(E)