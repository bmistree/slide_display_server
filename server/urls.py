from django.conf.urls.defaults import patterns, include, url
import views

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^index$','views.index',name='index'),
    url(r'^$','views.index',name='base'),
    url(r'^admin/', include(admin.site.urls) ),
    url(r'^check_reserved$','views.check_reserved',name='check_reserved'),
    url(r'^next_url$','views.next_url',name='next_url'),
    url(r'^resource_url$','views.resource_url',name='resource_url'),
)

