from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'testdjango.views.index', name='index'),
    url(r'testajax/', 'testdjango.views.testajax', name='testajax'),
    url(r'testautoreload/', 'testdjango.views.testautoreload', name='testautoreload'),
    #url(r'^$', TemplateView.as_view(template_name='base.html')),

    # Examples:
    # url(r'^$', 'testdjango.views.home', name='home'),
    # url(r'^$', 'testdjango.views.home', name='home'),
    # url(r'^testdjango/', include('testdjango.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
