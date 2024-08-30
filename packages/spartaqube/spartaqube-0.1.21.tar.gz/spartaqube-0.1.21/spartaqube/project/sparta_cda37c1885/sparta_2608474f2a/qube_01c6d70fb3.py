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
import project.sparta_509f9a5b62.sparta_76f284387c.qube_cb1c81c00b as qube_cb1c81c00b
from project.sparta_12b080e841.sparta_0687762cca.qube_90b70a692d import sparta_43a7ace2a8
from project.sparta_12b080e841.sparta_d2a912facc import qube_fe01c20cda as qube_fe01c20cda
@csrf_exempt
@sparta_43a7ace2a8
@login_required(redirect_field_name=_F)
def sparta_2a829d8640(request):
	B=request;C=B.GET.get('edit')
	if C is _B:C='-1'
	A=qube_cb1c81c00b.sparta_aca8f1d9a9(B);A[_C]=7;D=qube_cb1c81c00b.sparta_abf92cd2d9(B.user);A.update(D);A[_D]=_A;A['edit_chart_id']=C;return render(B,'dist/project/plot-db/plotDB.html',A)
@csrf_exempt
@sparta_43a7ace2a8
@login_required(redirect_field_name=_F)
def sparta_86ee771f9e(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_fe01c20cda.sparta_edcd0615ca(C,A.user);D=not E[_K]
	if D:return sparta_2a829d8640(A)
	B=qube_cb1c81c00b.sparta_aca8f1d9a9(A);B[_C]=7;F=qube_cb1c81c00b.sparta_abf92cd2d9(A.user);B.update(F);B[_D]=_A;B[_H]=C;G=E[_E];B[_I]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_43a7ace2a8
def sparta_ebbbee64bd(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return sparta_c0298837ed(A,B)
@csrf_exempt
@sparta_43a7ace2a8
def sparta_87f947e51e(request,widget_id,session_id,api_token_id):return sparta_c0298837ed(request,widget_id,session_id)
def sparta_c0298837ed(request,plot_chart_id,session='-1'):
	G='res';E=plot_chart_id;B=request;C=_G
	if E is _B:C=_A
	else:
		D=qube_fe01c20cda.sparta_42ab6eeecf(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_2a829d8640(B)
	A=qube_cb1c81c00b.sparta_aca8f1d9a9(B);A[_C]=7;I=qube_cb1c81c00b.sparta_abf92cd2d9(B.user);A.update(I);A[_D]=_A;F=D[_E];A['b_require_password']=0 if D[G]==1 else 1;A[_H]=F.plot_chart_id;A[_I]=F.name;A[_J]=str(session);return render(B,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
@sparta_43a7ace2a8
def sparta_22e7cf3a24(request,session_id,api_token_id):B=request;A=qube_cb1c81c00b.sparta_aca8f1d9a9(B);A[_C]=7;C=qube_cb1c81c00b.sparta_abf92cd2d9(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_43a7ace2a8
@login_required(redirect_field_name=_F)
def sparta_3c197ac8f1(request):
	J=',\n    ';B=request;C=B.GET.get('id');F=_G
	if C is _B:F=_A
	else:G=qube_fe01c20cda.sparta_edcd0615ca(C,B.user);F=not G[_K]
	if F:return sparta_2a829d8640(B)
	K=qube_fe01c20cda.sparta_254221267f(G[_E]);D='';H=0
	for(E,I)in K.items():
		if H>0:D+=J
		if I==1:D+=f"{E}=input_{E}"
		else:L=str(J.join([f"input_{E}_{A}"for A in range(I)]));D+=f"{E}=[{L}]"
		H+=1
	M=f'Spartaqube().get_widget(\n    "{C}"\n)';N=f'Spartaqube().plot_(\n    "{C}",\n    {D}\n)';A=qube_cb1c81c00b.sparta_aca8f1d9a9(B);A[_C]=7;O=qube_cb1c81c00b.sparta_abf92cd2d9(B.user);A.update(O);A[_D]=_A;A[_H]=C;P=G[_E];A[_I]=P.name;A['plot_data_cmd']=M;A['plot_data_cmd_inputs']=N;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_43a7ace2a8
def sparta_f3e4916cb8(request,session_id,api_token_id,json_vars_html):B=request;A=qube_cb1c81c00b.sparta_aca8f1d9a9(B);A[_C]=7;C=qube_cb1c81c00b.sparta_abf92cd2d9(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;A.update(json.loads(json_vars_html));return render(B,'dist/project/plot-db/plotAPI.html',A)