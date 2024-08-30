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
from project.sparta_12b080e841.sparta_6e8b6686d8 import qube_7a842d72ce as qube_7a842d72ce
from project.sparta_12b080e841.sparta_6e8b6686d8 import qube_cfa1605bf8 as qube_cfa1605bf8
from project.sparta_12b080e841.sparta_580d8c46ca import qube_95c6ce3efb as qube_95c6ce3efb
from project.sparta_12b080e841.sparta_0687762cca.qube_90b70a692d import sparta_47f2fcf87d
@csrf_exempt
@sparta_47f2fcf87d
def sparta_d51d599aa1(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_7a842d72ce.sparta_2d29778c42(E,A.user,B[D])
	else:C={_C:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_47f2fcf87d
def sparta_e8bb89f4bb(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_7a842d72ce.sparta_ed19e0b4c3(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_47f2fcf87d
def sparta_b92214c80f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_7a842d72ce.sparta_64c3164250(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_47f2fcf87d
def sparta_4ee96a7b01(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_7a842d72ce.sparta_bc2fab463e(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_47f2fcf87d
def sparta_66317a1f2d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_cfa1605bf8.sparta_9ce448c22b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_47f2fcf87d
def sparta_5513c877ba(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_7a842d72ce.sparta_ad633caa4b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_47f2fcf87d
def sparta_3ee6dc2b11(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_7a842d72ce.sparta_7471f26ed1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_47f2fcf87d
def sparta_36ca4ec622(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_7a842d72ce.sparta_b6da90c3db(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_47f2fcf87d
def sparta_ddc715893a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_7a842d72ce.sparta_c7396027b1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_47f2fcf87d
def sparta_07c079f019(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_7a842d72ce.sparta_645153446b(J,A.user)
	if C[_C]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_D]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_47f2fcf87d
def sparta_4454c052fd(request):
	E='folderName';C=request;F=C.GET[_B];D=C.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};B=qube_7a842d72ce.sparta_95beee7a83(G,C.user);print(_C);print(B)
	if B[_C]==1:H=B['zip'];I=B[_H];A=HttpResponse();A.write(H.getvalue());A[_D]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_D]=_F.format(K)
	return A
@csrf_exempt
@sparta_47f2fcf87d
def sparta_22ee22c72b(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_7a842d72ce.sparta_2efe172525(F,B.user)
	if C[_C]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_D]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_D]=_F.format(J)
	return A