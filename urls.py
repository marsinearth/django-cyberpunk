import os
from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include
from cyberpunk.views import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
admin.autodiscover()
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
admin.site.unregister(Group)
admin.site.unregister(Permission)

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',                       
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^$', main_page),
    (r'^admin/', include(admin.site.urls)),
#    (r'^admin/(\w+)/$',admin_page),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^user/$', user_page),
    (r'^user/edit/(?P<id>\d+)/$', useredit),
    (r'^character/(?P<charname>[\s|\S]+)/$', character_page), 
    (r'^logout/$', logout_page),
    (r'^register/$', register_page),
    (r'^register/success/$', direct_to_template,
      {'template': 'registration/register_success.djhtml'}),
    (r'^char/new/$', charedit, {}, 'char_new'),  
    (r'^char/edit/(?P<id>\d+)/$', charedit, {}, 'char_edit'),
    (r'^char/delete/(?P<id>\d+)/$', chardelete),                            
    (r'^obj/new/(?P<charname>[\s|\S]+)/(?P<category>\w+)/$', editobj, {}, 'obj_new'),  
    (r'^obj/edit/(?P<charname>[\s|\S]+)/(?P<category>\w+)/(?P<id>\d+)/$', editobj, {}, 'obj_edit'),
    (r'^obj/delete/(?P<charname>[\s|\S]+)/(?P<category>\w+)/(?P<id>\d+)/$', deleteobj),            
    (r'^obj/equip/(?P<charname>[\s|\S]+)/(?P<category>\w+)/(?P<id>\d+)/$', equipobj),              
    (r'^obj/unequip/(?P<charname>[\s|\S]+)/(?P<category>\w+)/(?P<id>\d+)/$', unequipobj),              
    # Examples:
    # url(r'^$', 'Cyberpunk.views.home', name='home'),
    # url(r'^Cyberpunk/', include('Cyberpunk.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
