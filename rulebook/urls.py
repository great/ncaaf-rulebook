from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'rulebook.views.home', name='home'),
    # url(r'^rulebook/', include('rulebook.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'rule.views.index', name='home'),
    url(r'^(?P<language>[A-Z][A-Z])/$', 'rule.views.index', name='chapter'),
    url(r'^chapter/(?P<language>[A-Z][A-Z])/$', 'rule.views.chapter', name='chapter'),
    #url(r'^(?P<rule_id>\d+)/$', 'rule.views.rule', name='each rule'),
    #url(r'^(?P<language>[A-Z][A-Z])/(?P<rule_id>\d+)/$', 'rule.views.each_rule', name='sections'),
    url(r'^article/(?P<language>[A-Z][A-Z])/(?P<meta_id>\d+)/$', 'rule.views.article', name='article'),
    url(r'^articles/(?P<language>[A-Z][A-Z])/(?P<rule_id>\d+)/(?P<section_id>\d+)/$', 'rule.views.articles', name='articles'),
)
