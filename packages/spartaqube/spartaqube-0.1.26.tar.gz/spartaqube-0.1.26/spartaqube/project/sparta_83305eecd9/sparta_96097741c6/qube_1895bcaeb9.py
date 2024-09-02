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
import project.sparta_b972c86658.sparta_741716a68d.qube_4982ec8d00 as qube_4982ec8d00
from project.sparta_55934fbdfb.sparta_db8b2eb16f.qube_da95fe36a3 import sparta_091e7a614b
from project.sparta_55934fbdfb.sparta_8d9d1db88d import qube_7c37f05664 as qube_7c37f05664
@csrf_exempt
@sparta_091e7a614b
@login_required(redirect_field_name=_F)
def sparta_b86350ea73(request):
	B=request;C=B.GET.get('edit')
	if C is _B:C='-1'
	A=qube_4982ec8d00.sparta_48cfdf4b1d(B);A[_C]=7;D=qube_4982ec8d00.sparta_6204b13016(B.user);A.update(D);A[_D]=_A;A['edit_chart_id']=C;return render(B,'dist/project/plot-db/plotDB.html',A)
@csrf_exempt
@sparta_091e7a614b
@login_required(redirect_field_name=_F)
def sparta_af2eb335de(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_7c37f05664.sparta_8b51600314(C,A.user);D=not E[_K]
	if D:return sparta_b86350ea73(A)
	B=qube_4982ec8d00.sparta_48cfdf4b1d(A);B[_C]=7;F=qube_4982ec8d00.sparta_6204b13016(A.user);B.update(F);B[_D]=_A;B[_H]=C;G=E[_E];B[_I]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_091e7a614b
def sparta_d424f7205d(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return sparta_46dfd14d32(A,B)
@csrf_exempt
@sparta_091e7a614b
def sparta_b27811ed17(request,widget_id,session_id,api_token_id):return sparta_46dfd14d32(request,widget_id,session_id)
def sparta_46dfd14d32(request,plot_chart_id,session='-1'):
	G='res';E=plot_chart_id;B=request;C=_G
	if E is _B:C=_A
	else:
		D=qube_7c37f05664.sparta_36d79254f5(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_b86350ea73(B)
	A=qube_4982ec8d00.sparta_48cfdf4b1d(B);A[_C]=7;I=qube_4982ec8d00.sparta_6204b13016(B.user);A.update(I);A[_D]=_A;F=D[_E];A['b_require_password']=0 if D[G]==1 else 1;A[_H]=F.plot_chart_id;A[_I]=F.name;A[_J]=str(session);return render(B,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
@sparta_091e7a614b
def sparta_57bc8b5779(request,session_id,api_token_id):B=request;A=qube_4982ec8d00.sparta_48cfdf4b1d(B);A[_C]=7;C=qube_4982ec8d00.sparta_6204b13016(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_091e7a614b
@login_required(redirect_field_name=_F)
def sparta_5fa3b514a3(request):
	J=',\n    ';B=request;C=B.GET.get('id');F=_G
	if C is _B:F=_A
	else:G=qube_7c37f05664.sparta_8b51600314(C,B.user);F=not G[_K]
	if F:return sparta_b86350ea73(B)
	K=qube_7c37f05664.sparta_2b13b37b74(G[_E]);D='';H=0
	for(E,I)in K.items():
		if H>0:D+=J
		if I==1:D+=f"{E}=input_{E}"
		else:L=str(J.join([f"input_{E}_{A}"for A in range(I)]));D+=f"{E}=[{L}]"
		H+=1
	M=f'Spartaqube().get_widget(\n    "{C}"\n)';N=f'Spartaqube().plot_(\n    "{C}",\n    {D}\n)';A=qube_4982ec8d00.sparta_48cfdf4b1d(B);A[_C]=7;O=qube_4982ec8d00.sparta_6204b13016(B.user);A.update(O);A[_D]=_A;A[_H]=C;P=G[_E];A[_I]=P.name;A['plot_data_cmd']=M;A['plot_data_cmd_inputs']=N;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_091e7a614b
def sparta_46186c8e48(request,session_id,api_token_id,json_vars_html):B=request;A=qube_4982ec8d00.sparta_48cfdf4b1d(B);A[_C]=7;C=qube_4982ec8d00.sparta_6204b13016(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;A.update(json.loads(json_vars_html));return render(B,'dist/project/plot-db/plotAPI.html',A)