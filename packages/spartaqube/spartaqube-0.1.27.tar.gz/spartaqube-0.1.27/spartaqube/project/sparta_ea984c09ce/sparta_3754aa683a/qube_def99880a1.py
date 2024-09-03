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
from project.sparta_c8e521c5f3.sparta_3f7efd553f import qube_2d9eac2fb4 as qube_2d9eac2fb4
from project.sparta_c8e521c5f3.sparta_3f7efd553f import qube_39d0d1973b as qube_39d0d1973b
from project.sparta_c8e521c5f3.sparta_0265a7530c import qube_eca803108e as qube_eca803108e
from project.sparta_c8e521c5f3.sparta_bc89190359.qube_6059f885cd import sparta_f8d86bc838
@csrf_exempt
@sparta_f8d86bc838
def sparta_ebe4ece4fc(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_2d9eac2fb4.sparta_bfd97aba4e(E,A.user,B[D])
	else:C={_C:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_f8d86bc838
def sparta_6a03a51e8e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2d9eac2fb4.sparta_8d28b9f722(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f8d86bc838
def sparta_45b28516f7(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2d9eac2fb4.sparta_3a31229822(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f8d86bc838
def sparta_47ce8f1287(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2d9eac2fb4.sparta_4a0ac87cdc(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f8d86bc838
def sparta_dd96651c2d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_39d0d1973b.sparta_55be08ab34(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f8d86bc838
def sparta_e29079b158(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2d9eac2fb4.sparta_d8cdba3b47(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f8d86bc838
def sparta_2b59652f59(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2d9eac2fb4.sparta_75168df132(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f8d86bc838
def sparta_d864d5d441(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2d9eac2fb4.sparta_9d595188f6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f8d86bc838
def sparta_10df4c4cf3(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_2d9eac2fb4.sparta_5e133d3d20(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_f8d86bc838
def sparta_3c3b90e2ea(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_2d9eac2fb4.sparta_1ccb9f58d5(J,A.user)
	if C[_C]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_D]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_f8d86bc838
def sparta_c56a8421a3(request):
	E='folderName';C=request;F=C.GET[_B];D=C.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};B=qube_2d9eac2fb4.sparta_45933f223d(G,C.user);print(_C);print(B)
	if B[_C]==1:H=B['zip'];I=B[_H];A=HttpResponse();A.write(H.getvalue());A[_D]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_D]=_F.format(K)
	return A
@csrf_exempt
@sparta_f8d86bc838
def sparta_92ed123b03(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_2d9eac2fb4.sparta_5a97eacd3e(F,B.user)
	if C[_C]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_D]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_D]=_F.format(J)
	return A