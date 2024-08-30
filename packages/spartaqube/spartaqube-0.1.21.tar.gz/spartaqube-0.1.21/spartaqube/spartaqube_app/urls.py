from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_cda37c1885.sparta_0c06255e3d.qube_0cc21dbc97.sparta_a6df8058f4'
handler500='project.sparta_cda37c1885.sparta_0c06255e3d.qube_0cc21dbc97.sparta_0def548297'
handler403='project.sparta_cda37c1885.sparta_0c06255e3d.qube_0cc21dbc97.sparta_fc22b23ed7'
handler400='project.sparta_cda37c1885.sparta_0c06255e3d.qube_0cc21dbc97.sparta_9b3b4be40f'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]