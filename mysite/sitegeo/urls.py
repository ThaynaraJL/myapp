from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sitegeo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', 'myapp.views.index', name='myapp_index'),
    url(r'^processa/$', 'myapp.views.processo', name='myapp_processo'),
 	url(r'^style/$', 'myapp.views.style', name='myapp_style'),
    url(r'^jquery/$', 'myapp.views.jquery', name='myapp_jquery'),
    url(r'^poligono/$', 'myapp.views.poligono', name='myapp_poligono'),
    url(r'^processar/$', 'myapp.views.processar', name='myapp_processar'),
    url(r'^compara/$','myapp.views.compara', name='myapp_compara'),
    url(r'^geocoding/$', 'myapp.views.geocoding', name='myapp_geocoding'),
    url(r'^teste/$', 'myapp.views.teste', name='myapp_teste'),
    url(r'^exibeinfracoes/$', 'myapp.views.exibeinfracoes', name='myapp_exibeinfracoes'),




)
