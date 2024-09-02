_K='has_access'
_J='session'
_I='plot_name'
_H='plot_chart_id'
_G=False
_F='login'
_E='plot_db_chart_obj'
_D='bCodeMirror'
_C='menuBar'
_B=None
_A=True
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_d7b94e3744.sparta_cc6e9d39f9.qube_707ef4ff5f as qube_707ef4ff5f
from project.sparta_40ba2b27bc.sparta_5da2ea1aa8.qube_816b9a59f8 import sparta_42f3fead5c
from project.sparta_40ba2b27bc.sparta_ffa6b80cbc import qube_8c9113b621 as qube_8c9113b621
@csrf_exempt
@sparta_42f3fead5c
@login_required(redirect_field_name=_F)
def sparta_dd474c4c9e(request):
	B=request;C=B.GET.get('edit')
	if C is _B:C='-1'
	A=qube_707ef4ff5f.sparta_d9406e4da5(B);A[_C]=7;D=qube_707ef4ff5f.sparta_d157c2d07e(B.user);A.update(D);A[_D]=_A;A['edit_chart_id']=C;return render(B,'dist/project/plot-db/plotDB.html',A)
@csrf_exempt
@sparta_42f3fead5c
@login_required(redirect_field_name=_F)
def sparta_647a065375(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_8c9113b621.sparta_a0da48c65e(C,A.user);D=not E[_K]
	if D:return sparta_dd474c4c9e(A)
	B=qube_707ef4ff5f.sparta_d9406e4da5(A);B[_C]=7;F=qube_707ef4ff5f.sparta_d157c2d07e(A.user);B.update(F);B[_D]=_A;B[_H]=C;G=E[_E];B[_I]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_42f3fead5c
def sparta_4ac0038d52(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return sparta_de318e7093(A,B)
@csrf_exempt
@sparta_42f3fead5c
def sparta_80b060cd49(request,widget_id,session_id,api_token_id):return sparta_de318e7093(request,widget_id,session_id)
def sparta_de318e7093(request,plot_chart_id,session='-1'):
	G='res';E=plot_chart_id;B=request;C=_G
	if E is _B:C=_A
	else:
		D=qube_8c9113b621.sparta_52b6a93721(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_dd474c4c9e(B)
	A=qube_707ef4ff5f.sparta_d9406e4da5(B);A[_C]=7;I=qube_707ef4ff5f.sparta_d157c2d07e(B.user);A.update(I);A[_D]=_A;F=D[_E];A['b_require_password']=0 if D[G]==1 else 1;A[_H]=F.plot_chart_id;A[_I]=F.name;A[_J]=str(session);return render(B,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
@sparta_42f3fead5c
def sparta_b31adbfcc9(request,session_id,api_token_id):B=request;A=qube_707ef4ff5f.sparta_d9406e4da5(B);A[_C]=7;C=qube_707ef4ff5f.sparta_d157c2d07e(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_42f3fead5c
@login_required(redirect_field_name=_F)
def sparta_e0c460e939(request):
	J=',\n    ';B=request;C=B.GET.get('id');F=_G
	if C is _B:F=_A
	else:G=qube_8c9113b621.sparta_a0da48c65e(C,B.user);F=not G[_K]
	if F:return sparta_dd474c4c9e(B)
	K=qube_8c9113b621.sparta_e0017a61c9(G[_E]);D='';H=0
	for(E,I)in K.items():
		if H>0:D+=J
		if I==1:D+=f"{E}=input_{E}"
		else:L=str(J.join([f"input_{E}_{A}"for A in range(I)]));D+=f"{E}=[{L}]"
		H+=1
	M=f'Spartaqube().get_widget(\n    "{C}"\n)';N=f'Spartaqube().plot_(\n    "{C}",\n    {D}\n)';A=qube_707ef4ff5f.sparta_d9406e4da5(B);A[_C]=7;O=qube_707ef4ff5f.sparta_d157c2d07e(B.user);A.update(O);A[_D]=_A;A[_H]=C;P=G[_E];A[_I]=P.name;A['plot_data_cmd']=M;A['plot_data_cmd_inputs']=N;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_42f3fead5c
def sparta_8bb1be2787(request,session_id,api_token_id,json_vars_html):B=request;A=qube_707ef4ff5f.sparta_d9406e4da5(B);A[_C]=7;C=qube_707ef4ff5f.sparta_d157c2d07e(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;A.update(json.loads(json_vars_html));return render(B,'dist/project/plot-db/plotAPI.html',A)