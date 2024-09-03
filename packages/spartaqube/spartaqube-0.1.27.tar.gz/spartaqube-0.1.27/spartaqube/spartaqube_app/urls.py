from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_b9d232118a.sparta_51ec45343d.qube_e926133552.sparta_dbe6eb28b5'
handler500='project.sparta_b9d232118a.sparta_51ec45343d.qube_e926133552.sparta_3e797933af'
handler403='project.sparta_b9d232118a.sparta_51ec45343d.qube_e926133552.sparta_5e09a5f190'
handler400='project.sparta_b9d232118a.sparta_51ec45343d.qube_e926133552.sparta_fdff9392e6'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]