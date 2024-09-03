import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_c8e521c5f3.sparta_66a5db445d import qube_85a0d06138 as qube_85a0d06138
from project.sparta_c8e521c5f3.sparta_bc89190359.qube_6059f885cd import sparta_f8d86bc838
@csrf_exempt
@sparta_f8d86bc838
def sparta_9b3691b2e9(request):G='api_func';F='key';E='utf-8';A=request;C=A.body.decode(E);C=A.POST.get(F);D=A.body.decode(E);D=A.POST.get(G);B=dict();B[F]=C;B[G]=D;H=qube_85a0d06138.sparta_9b3691b2e9(B,A.user);I=json.dumps(H);return HttpResponse(I)