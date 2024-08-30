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
from project.sparta_12b080e841.sparta_f3e8e5375c import qube_c9bc1481ca as qube_c9bc1481ca
from project.sparta_12b080e841.sparta_0687762cca.qube_90b70a692d import sparta_47f2fcf87d
@csrf_exempt
@sparta_47f2fcf87d
def sparta_b0a78390f1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c9bc1481ca.sparta_b0a78390f1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_47f2fcf87d
def sparta_c888c0564d(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_c9bc1481ca.sparta_c888c0564d(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_47f2fcf87d
def sparta_80979d78b7(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_c9bc1481ca.sparta_80979d78b7(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_47f2fcf87d
def sparta_7392aaa353(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c9bc1481ca.sparta_7392aaa353(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_47f2fcf87d
def sparta_2fa4145eaa(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c9bc1481ca.sparta_2fa4145eaa(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_47f2fcf87d
def sparta_d3a23e0915(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c9bc1481ca.sparta_d3a23e0915(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_4d0884d6fb(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_c9bc1481ca.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_47f2fcf87d
def sparta_b7120e451e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c9bc1481ca.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_45e81bf558(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_c9bc1481ca.sparta_45e81bf558(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_11c862d4b4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c9bc1481ca.sparta_11c862d4b4(A,C);E=json.dumps(D);return HttpResponse(E)