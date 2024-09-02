from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_83305eecd9.sparta_ff182cfdda.qube_372b7481fb.sparta_3551f1b69f'
handler500='project.sparta_83305eecd9.sparta_ff182cfdda.qube_372b7481fb.sparta_78a8eaea87'
handler403='project.sparta_83305eecd9.sparta_ff182cfdda.qube_372b7481fb.sparta_46acd1c4b1'
handler400='project.sparta_83305eecd9.sparta_ff182cfdda.qube_372b7481fb.sparta_260d2d7629'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]