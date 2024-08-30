from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings as conf_settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import hashlib,project.sparta_509f9a5b62.sparta_76f284387c.qube_cb1c81c00b as qube_cb1c81c00b
from project.sparta_12b080e841.sparta_0687762cca.qube_90b70a692d import sparta_43a7ace2a8
@csrf_exempt
def sparta_1692854635(request):B=request;A=qube_cb1c81c00b.sparta_aca8f1d9a9(B);A['menuBar']=8;A['bCodeMirror']=True;C=qube_cb1c81c00b.sparta_abf92cd2d9(B.user);A.update(C);return render(B,'dist/project/api/api.html',A)