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
from project.sparta_30e2c8fafc.sparta_b3a3f99282 import qube_19fd4b7022 as qube_19fd4b7022
from project.sparta_30e2c8fafc.sparta_b3a3f99282 import qube_196b2cb8e0 as qube_196b2cb8e0
from project.sparta_30e2c8fafc.sparta_e8608fa6bc import qube_e278700345 as qube_e278700345
from project.sparta_30e2c8fafc.sparta_4f7fa902d8.qube_b0ccd99581 import sparta_25b99b49dd
@csrf_exempt
@sparta_25b99b49dd
def sparta_dbe6a30be1(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_19fd4b7022.sparta_85486165a0(E,A.user,B[D])
	else:C={_C:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_25b99b49dd
def sparta_b4a5b29c5b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_19fd4b7022.sparta_2d83d85efa(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_25b99b49dd
def sparta_b1dc37bd72(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_19fd4b7022.sparta_7084af2d7f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_25b99b49dd
def sparta_f78d00d5f7(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_19fd4b7022.sparta_95ea0773c3(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_25b99b49dd
def sparta_e7b6b84840(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_196b2cb8e0.sparta_2ed0b6f2ca(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_25b99b49dd
def sparta_a0f9b55171(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_19fd4b7022.sparta_60a1403af6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_25b99b49dd
def sparta_9071f6b24a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_19fd4b7022.sparta_69eff5f403(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_25b99b49dd
def sparta_ef17c52ca7(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_19fd4b7022.sparta_2a0bb249a7(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_25b99b49dd
def sparta_3885e96510(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_19fd4b7022.sparta_c2921df74b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_25b99b49dd
def sparta_1d86d6200c(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_19fd4b7022.sparta_96340e7054(J,A.user)
	if C[_C]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_D]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_25b99b49dd
def sparta_0be2a70985(request):
	E='folderName';C=request;F=C.GET[_B];D=C.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};B=qube_19fd4b7022.sparta_ca693f2517(G,C.user);print(_C);print(B)
	if B[_C]==1:H=B['zip'];I=B[_H];A=HttpResponse();A.write(H.getvalue());A[_D]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_D]=_F.format(K)
	return A
@csrf_exempt
@sparta_25b99b49dd
def sparta_36bbf63526(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_19fd4b7022.sparta_9740c8ae04(F,B.user)
	if C[_C]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_D]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_D]=_F.format(J)
	return A