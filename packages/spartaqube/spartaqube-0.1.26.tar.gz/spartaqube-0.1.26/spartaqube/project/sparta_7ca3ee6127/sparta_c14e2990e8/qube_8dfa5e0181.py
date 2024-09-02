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
from project.sparta_55934fbdfb.sparta_e417995ea0 import qube_d41cdef6bb as qube_d41cdef6bb
from project.sparta_55934fbdfb.sparta_e417995ea0 import qube_303013033b as qube_303013033b
from project.sparta_55934fbdfb.sparta_ce3abe84ce import qube_e97887f5fc as qube_e97887f5fc
from project.sparta_55934fbdfb.sparta_db8b2eb16f.qube_da95fe36a3 import sparta_2dd23776f5
@csrf_exempt
@sparta_2dd23776f5
def sparta_fdbe8ee56b(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_d41cdef6bb.sparta_691dbecda1(E,A.user,B[D])
	else:C={_C:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_2dd23776f5
def sparta_1c7762d0fa(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d41cdef6bb.sparta_6199052c82(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2dd23776f5
def sparta_22d5b467c1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d41cdef6bb.sparta_5e903e940e(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2dd23776f5
def sparta_8e953e8209(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d41cdef6bb.sparta_13cdbfccd9(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2dd23776f5
def sparta_bd6771f6d9(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_303013033b.sparta_7b5edf07bf(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2dd23776f5
def sparta_cad55b99de(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d41cdef6bb.sparta_bb44ae397b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2dd23776f5
def sparta_f032299a81(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d41cdef6bb.sparta_38b3757478(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2dd23776f5
def sparta_9270778509(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d41cdef6bb.sparta_c6f3cfc10c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2dd23776f5
def sparta_c154691db6(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d41cdef6bb.sparta_78b030bc7d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_2dd23776f5
def sparta_3be820b748(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_d41cdef6bb.sparta_6fe9d328bd(J,A.user)
	if C[_C]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_D]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_2dd23776f5
def sparta_0c5852cb86(request):
	E='folderName';C=request;F=C.GET[_B];D=C.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};B=qube_d41cdef6bb.sparta_ad1fd7c1ba(G,C.user);print(_C);print(B)
	if B[_C]==1:H=B['zip'];I=B[_H];A=HttpResponse();A.write(H.getvalue());A[_D]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_D]=_F.format(K)
	return A
@csrf_exempt
@sparta_2dd23776f5
def sparta_f8cb865ad9(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_d41cdef6bb.sparta_77c6be473d(F,B.user)
	if C[_C]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_D]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_D]=_F.format(J)
	return A