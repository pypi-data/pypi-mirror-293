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
from project.sparta_40ba2b27bc.sparta_c7170c273b import qube_d275611067 as qube_d275611067
from project.sparta_40ba2b27bc.sparta_5da2ea1aa8.qube_816b9a59f8 import sparta_59f81fc832
@csrf_exempt
@sparta_59f81fc832
def sparta_141303b7bf(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d275611067.sparta_141303b7bf(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_59f81fc832
def sparta_8a6bec5eb7(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_d275611067.sparta_8a6bec5eb7(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_59f81fc832
def sparta_a179f319a1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_d275611067.sparta_a179f319a1(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_59f81fc832
def sparta_a268a66528(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d275611067.sparta_a268a66528(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_59f81fc832
def sparta_fe59e8d13f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d275611067.sparta_fe59e8d13f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_59f81fc832
def sparta_73c15dde47(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d275611067.sparta_73c15dde47(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_1e6b10e904(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_d275611067.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_59f81fc832
def sparta_ce83c46007(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d275611067.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_92ce54700e(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_d275611067.sparta_92ce54700e(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_bcf227f400(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d275611067.sparta_bcf227f400(A,C);E=json.dumps(D);return HttpResponse(E)