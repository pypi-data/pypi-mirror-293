import pkg_resources
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import re_path as url
from django.conf import settings
from project.sparta_3ca0064d9b.sparta_d64cb5e4b9 import qube_73bb9f8956,qube_522bb8c317,qube_72750c5af0
from channels.auth import AuthMiddlewareStack
import channels
channels_ver=pkg_resources.get_distribution('channels').version
channels_major=int(channels_ver.split('.')[0])
print('CHANNELS VERSION')
print(channels_ver)
def sparta_77ab76a018(this_class):
	A=this_class
	if channels_major<=2:return A
	else:return A.as_asgi()
urlpatterns=[url('ws/statusWS',sparta_77ab76a018(qube_73bb9f8956.StatusWS)),url('ws/notebookWS',sparta_77ab76a018(qube_522bb8c317.NotebookWS)),url('ws/wssConnectorWS',sparta_77ab76a018(qube_72750c5af0.WssConnectorWS))]
application=ProtocolTypeRouter({'websocket':AuthMiddlewareStack(URLRouter(urlpatterns))})
for thisUrlPattern in urlpatterns:
	try:
		if len(settings.DAPHNE_PREFIX)>0:thisUrlPattern.pattern._regex='^'+settings.DAPHNE_PREFIX+'/'+thisUrlPattern.pattern._regex
	except Exception as e:print(e)