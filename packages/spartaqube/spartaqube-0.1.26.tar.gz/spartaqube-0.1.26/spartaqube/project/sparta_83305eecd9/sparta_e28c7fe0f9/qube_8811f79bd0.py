from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings as conf_settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import hashlib,project.sparta_b972c86658.sparta_741716a68d.qube_4982ec8d00 as qube_4982ec8d00
from project.sparta_55934fbdfb.sparta_db8b2eb16f.qube_da95fe36a3 import sparta_091e7a614b
@csrf_exempt
def sparta_2389947736(request):B=request;A=qube_4982ec8d00.sparta_48cfdf4b1d(B);A['menuBar']=8;A['bCodeMirror']=True;C=qube_4982ec8d00.sparta_6204b13016(B.user);A.update(C);return render(B,'dist/project/api/api.html',A)