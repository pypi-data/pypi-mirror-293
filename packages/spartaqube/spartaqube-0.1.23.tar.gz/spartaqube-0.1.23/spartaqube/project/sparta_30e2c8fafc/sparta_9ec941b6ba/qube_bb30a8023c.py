from datetime import datetime
import hashlib,os,sys,django
from django.utils.text import slugify
def sparta_34b0daf41b():C='/';B='\\';D=os.path.dirname(os.path.abspath(__file__)).replace(B,C);A=os.path.dirname(D).replace(B,C);A=os.path.dirname(A).replace(B,C);A=os.path.dirname(A).replace(B,C);sys.path.append(A);print('oneLevelUpPath');print(A);os.environ.setdefault('DJANGO_SETTINGS_MODULE','spartaqube_app.settings');os.environ['DJANGO_ALLOW_ASYNC_UNSAFE']='true';django.setup()
def sparta_3beb9ecc6a():
	from django.contrib.auth.models import User;from project.models import UserProfile,PlotDBChart as C;F=C.objects.all()
	for B in F:
		if B.slug is None:
			A=B.name;D=slugify(A);A=D;E=1
			while C.objects.filter(slug=A).exists():A=f"{D}-{E}";E+=1
			print('slug');print(A);B.slug=A;B.save()
if __name__=='__main__':sparta_34b0daf41b();qube_bb30a8023c()