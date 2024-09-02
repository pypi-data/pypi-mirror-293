_I='error.txt'
_H='zipName'
_G='utf-8'
_F='attachment; filename={0}'
_E='appId'
_D='Content-Disposition'
_C='res'
_B='projectPath'
_A='jsonData'
import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_40ba2b27bc.sparta_13b3a97337 import qube_70da457bf1 as qube_70da457bf1
from project.sparta_40ba2b27bc.sparta_13b3a97337 import qube_e26a97bae5 as qube_e26a97bae5
from project.sparta_40ba2b27bc.sparta_dc05d02cc2 import qube_0377b9b446 as qube_0377b9b446
from project.sparta_40ba2b27bc.sparta_5da2ea1aa8.qube_816b9a59f8 import sparta_59f81fc832
@csrf_exempt
@sparta_59f81fc832
def sparta_4415da8a83(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_70da457bf1.sparta_efe974ed80(E,A.user,B[D])
	else:C={_C:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_59f81fc832
def sparta_09915cd567(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_70da457bf1.sparta_426a210916(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_59f81fc832
def sparta_a7259914fc(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_70da457bf1.sparta_614c02619d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_59f81fc832
def sparta_057aa2433b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_70da457bf1.sparta_bd63b1538f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_59f81fc832
def sparta_cb28cf8194(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_e26a97bae5.sparta_7826a46da7(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_59f81fc832
def sparta_be19f61958(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_70da457bf1.sparta_e9b4453dee(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_59f81fc832
def sparta_6c88c74a18(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_70da457bf1.sparta_1e631acff3(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_59f81fc832
def sparta_fbc764c93b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_70da457bf1.sparta_34819ba636(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_59f81fc832
def sparta_045badfb6f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_70da457bf1.sparta_ba012ad56d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_59f81fc832
def sparta_fdca7e6d52(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_70da457bf1.sparta_bfdf999f1d(J,A.user)
	if C[_C]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_D]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_59f81fc832
def sparta_75d054da69(request):
	E='folderName';C=request;F=C.GET[_B];D=C.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};B=qube_70da457bf1.sparta_61f64167c8(G,C.user);print(_C);print(B)
	if B[_C]==1:H=B['zip'];I=B[_H];A=HttpResponse();A.write(H.getvalue());A[_D]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_D]=_F.format(K)
	return A
@csrf_exempt
@sparta_59f81fc832
def sparta_57b3b10a67(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_70da457bf1.sparta_bf3fa7c75c(F,B.user)
	if C[_C]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_D]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_D]=_F.format(J)
	return A