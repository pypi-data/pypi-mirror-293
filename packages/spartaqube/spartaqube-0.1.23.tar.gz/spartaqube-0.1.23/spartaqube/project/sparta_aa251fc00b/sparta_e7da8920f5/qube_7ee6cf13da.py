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
import project.sparta_9cf3fbfd16.sparta_527aa3c9b5.qube_8fc5e0b148 as qube_8fc5e0b148
from project.sparta_30e2c8fafc.sparta_4f7fa902d8.qube_b0ccd99581 import sparta_7e621e226c
from project.sparta_30e2c8fafc.sparta_2bc13df85d import qube_a1e444584f as qube_a1e444584f
@csrf_exempt
@sparta_7e621e226c
@login_required(redirect_field_name=_F)
def sparta_1269d626b3(request):
	B=request;C=B.GET.get('edit')
	if C is _B:C='-1'
	A=qube_8fc5e0b148.sparta_5c9f39e944(B);A[_C]=7;D=qube_8fc5e0b148.sparta_31ee8ccaef(B.user);A.update(D);A[_D]=_A;A['edit_chart_id']=C;return render(B,'dist/project/plot-db/plotDB.html',A)
@csrf_exempt
@sparta_7e621e226c
@login_required(redirect_field_name=_F)
def sparta_680eb76bee(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_a1e444584f.sparta_8a016f94f4(C,A.user);D=not E[_K]
	if D:return sparta_1269d626b3(A)
	B=qube_8fc5e0b148.sparta_5c9f39e944(A);B[_C]=7;F=qube_8fc5e0b148.sparta_31ee8ccaef(A.user);B.update(F);B[_D]=_A;B[_H]=C;G=E[_E];B[_I]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_7e621e226c
def sparta_18ef3189c3(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return sparta_7c3c57d628(A,B)
@csrf_exempt
@sparta_7e621e226c
def sparta_124ff539bf(request,widget_id,session_id,api_token_id):return sparta_7c3c57d628(request,widget_id,session_id)
def sparta_7c3c57d628(request,plot_chart_id,session='-1'):
	G='res';E=plot_chart_id;B=request;C=_G
	if E is _B:C=_A
	else:
		D=qube_a1e444584f.sparta_9c64b54611(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_1269d626b3(B)
	A=qube_8fc5e0b148.sparta_5c9f39e944(B);A[_C]=7;I=qube_8fc5e0b148.sparta_31ee8ccaef(B.user);A.update(I);A[_D]=_A;F=D[_E];A['b_require_password']=0 if D[G]==1 else 1;A[_H]=F.plot_chart_id;A[_I]=F.name;A[_J]=str(session);return render(B,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
@sparta_7e621e226c
def sparta_3559416102(request,session_id,api_token_id):B=request;A=qube_8fc5e0b148.sparta_5c9f39e944(B);A[_C]=7;C=qube_8fc5e0b148.sparta_31ee8ccaef(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_7e621e226c
@login_required(redirect_field_name=_F)
def sparta_1c1521ef09(request):
	J=',\n    ';B=request;C=B.GET.get('id');F=_G
	if C is _B:F=_A
	else:G=qube_a1e444584f.sparta_8a016f94f4(C,B.user);F=not G[_K]
	if F:return sparta_1269d626b3(B)
	K=qube_a1e444584f.sparta_d0553c1849(G[_E]);D='';H=0
	for(E,I)in K.items():
		if H>0:D+=J
		if I==1:D+=f"{E}=input_{E}"
		else:L=str(J.join([f"input_{E}_{A}"for A in range(I)]));D+=f"{E}=[{L}]"
		H+=1
	M=f'Spartaqube().get_widget(\n    "{C}"\n)';N=f'Spartaqube().plot_(\n    "{C}",\n    {D}\n)';A=qube_8fc5e0b148.sparta_5c9f39e944(B);A[_C]=7;O=qube_8fc5e0b148.sparta_31ee8ccaef(B.user);A.update(O);A[_D]=_A;A[_H]=C;P=G[_E];A[_I]=P.name;A['plot_data_cmd']=M;A['plot_data_cmd_inputs']=N;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_7e621e226c
def sparta_a6f9fa833e(request,session_id,api_token_id,json_vars_html):B=request;A=qube_8fc5e0b148.sparta_5c9f39e944(B);A[_C]=7;C=qube_8fc5e0b148.sparta_31ee8ccaef(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;A.update(json.loads(json_vars_html));return render(B,'dist/project/plot-db/plotAPI.html',A)