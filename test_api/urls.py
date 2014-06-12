from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

## http://127.0.0.1/test_case/listener/83294628asdjh

urlpatterns = patterns('',
    # Examples:
    
    
    url(r'^$', 'test_api.views.home', name='home'),
    
    url(r'^profile$', 'test_api.views.profile'),
    url(r'^create_test_case$', 'test_api.views.create_test_case'),
    
    url(r'^test_case/(?P<test_case_id>.*)/create_listener$', 'test_api.views.create_listener'),
    url(r'^test_case/listener/(?P<unique_id>.*)$', 'test_api.views.hit_the_listener'),
    
    url(r'^test_case/create_request$', 'test_api.views.create_request'),
    

    url(r'^admin/', include(admin.site.urls)),
)


