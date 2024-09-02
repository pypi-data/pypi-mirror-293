from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_55af41a040.sparta_e8b1a281d6.qube_5907c4782a.sparta_f464d232e2'
handler500='project.sparta_55af41a040.sparta_e8b1a281d6.qube_5907c4782a.sparta_48e89289a3'
handler403='project.sparta_55af41a040.sparta_e8b1a281d6.qube_5907c4782a.sparta_c876d8a3e8'
handler400='project.sparta_55af41a040.sparta_e8b1a281d6.qube_5907c4782a.sparta_c3f19adc96'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]