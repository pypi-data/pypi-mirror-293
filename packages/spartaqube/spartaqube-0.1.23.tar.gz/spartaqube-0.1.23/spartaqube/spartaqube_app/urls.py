from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_aa251fc00b.sparta_98baa3e12e.qube_fb836ea5b6.sparta_f0427f60fb'
handler500='project.sparta_aa251fc00b.sparta_98baa3e12e.qube_fb836ea5b6.sparta_1fd5dee95b'
handler403='project.sparta_aa251fc00b.sparta_98baa3e12e.qube_fb836ea5b6.sparta_61267db808'
handler400='project.sparta_aa251fc00b.sparta_98baa3e12e.qube_fb836ea5b6.sparta_f900fca3c2'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]