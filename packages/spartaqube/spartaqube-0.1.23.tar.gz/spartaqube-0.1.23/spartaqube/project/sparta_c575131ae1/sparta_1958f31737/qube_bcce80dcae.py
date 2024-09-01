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
from project.sparta_30e2c8fafc.sparta_e4c749f896 import qube_a467ae9a61 as qube_a467ae9a61
from project.sparta_30e2c8fafc.sparta_4f7fa902d8.qube_b0ccd99581 import sparta_25b99b49dd
@csrf_exempt
@sparta_25b99b49dd
def sparta_38b5016fbb(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a467ae9a61.sparta_38b5016fbb(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_25b99b49dd
def sparta_bd47a101d4(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_a467ae9a61.sparta_bd47a101d4(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_25b99b49dd
def sparta_d89fb1ca48(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_a467ae9a61.sparta_d89fb1ca48(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_25b99b49dd
def sparta_708e9cf40f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a467ae9a61.sparta_708e9cf40f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_25b99b49dd
def sparta_1001828985(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a467ae9a61.sparta_1001828985(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_25b99b49dd
def sparta_15013004d2(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a467ae9a61.sparta_15013004d2(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_4ec3082dde(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_a467ae9a61.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_25b99b49dd
def sparta_12da8f58d9(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a467ae9a61.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_55b9a6f6d9(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_a467ae9a61.sparta_55b9a6f6d9(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_5868e34167(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a467ae9a61.sparta_5868e34167(A,C);E=json.dumps(D);return HttpResponse(E)