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
import project.sparta_3ca0064d9b.sparta_e277eee10c.qube_b6b724ff27 as qube_b6b724ff27
from project.sparta_c8e521c5f3.sparta_bc89190359.qube_6059f885cd import sparta_25d3a2863e
from project.sparta_c8e521c5f3.sparta_1506e63207 import qube_ded087e4e3 as qube_ded087e4e3
@csrf_exempt
@sparta_25d3a2863e
@login_required(redirect_field_name=_F)
def sparta_b19d3b862a(request):
	B=request;C=B.GET.get('edit')
	if C is _B:C='-1'
	A=qube_b6b724ff27.sparta_673b1c1989(B);A[_C]=7;D=qube_b6b724ff27.sparta_20838164ba(B.user);A.update(D);A[_D]=_A;A['edit_chart_id']=C;return render(B,'dist/project/plot-db/plotDB.html',A)
@csrf_exempt
@sparta_25d3a2863e
@login_required(redirect_field_name=_F)
def sparta_10b2a57f40(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_ded087e4e3.sparta_f1f3eaa0f3(C,A.user);D=not E[_K]
	if D:return sparta_b19d3b862a(A)
	B=qube_b6b724ff27.sparta_673b1c1989(A);B[_C]=7;F=qube_b6b724ff27.sparta_20838164ba(A.user);B.update(F);B[_D]=_A;B[_H]=C;G=E[_E];B[_I]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_25d3a2863e
def sparta_21fc389787(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return sparta_c6a62eefa4(A,B)
@csrf_exempt
@sparta_25d3a2863e
def sparta_ff963d8672(request,widget_id,session_id,api_token_id):return sparta_c6a62eefa4(request,widget_id,session_id)
def sparta_c6a62eefa4(request,plot_chart_id,session='-1'):
	G='res';E=plot_chart_id;B=request;C=_G
	if E is _B:C=_A
	else:
		D=qube_ded087e4e3.sparta_ed37f36c8a(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_b19d3b862a(B)
	A=qube_b6b724ff27.sparta_673b1c1989(B);A[_C]=7;I=qube_b6b724ff27.sparta_20838164ba(B.user);A.update(I);A[_D]=_A;F=D[_E];A['b_require_password']=0 if D[G]==1 else 1;A[_H]=F.plot_chart_id;A[_I]=F.name;A[_J]=str(session);return render(B,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
@sparta_25d3a2863e
def sparta_365de7553e(request,session_id,api_token_id):B=request;A=qube_b6b724ff27.sparta_673b1c1989(B);A[_C]=7;C=qube_b6b724ff27.sparta_20838164ba(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_25d3a2863e
@login_required(redirect_field_name=_F)
def sparta_54376d28f3(request):
	J=',\n    ';B=request;C=B.GET.get('id');F=_G
	if C is _B:F=_A
	else:G=qube_ded087e4e3.sparta_f1f3eaa0f3(C,B.user);F=not G[_K]
	if F:return sparta_b19d3b862a(B)
	K=qube_ded087e4e3.sparta_073b7cba80(G[_E]);D='';H=0
	for(E,I)in K.items():
		if H>0:D+=J
		if I==1:D+=f"{E}=input_{E}"
		else:L=str(J.join([f"input_{E}_{A}"for A in range(I)]));D+=f"{E}=[{L}]"
		H+=1
	M=f'Spartaqube().get_widget(\n    "{C}"\n)';N=f'Spartaqube().plot_(\n    "{C}",\n    {D}\n)';A=qube_b6b724ff27.sparta_673b1c1989(B);A[_C]=7;O=qube_b6b724ff27.sparta_20838164ba(B.user);A.update(O);A[_D]=_A;A[_H]=C;P=G[_E];A[_I]=P.name;A['plot_data_cmd']=M;A['plot_data_cmd_inputs']=N;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_25d3a2863e
def sparta_d57d16c9b3(request,session_id,api_token_id,json_vars_html):B=request;A=qube_b6b724ff27.sparta_673b1c1989(B);A[_C]=7;C=qube_b6b724ff27.sparta_20838164ba(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;A.update(json.loads(json_vars_html));return render(B,'dist/project/plot-db/plotAPI.html',A)