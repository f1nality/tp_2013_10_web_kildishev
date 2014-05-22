from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'helpme.views.home', name='home'),
    # url(r'^helpme/', include('helpme.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^mysql/fill/?$', 'ask.mysql.fill'),
    url(r'^((?P<tab>index|popular)/?((?P<page>[\d]+)/?)?)?$', 'ask.render.index'),
    url(r'^question/(?P<id>[\d]+)/?$', 'ask.render.question'),
    url(r'^user/(?P<id>[\d]+)/?$', 'ask.render.user'),
    url(r'^ajax/question_like/(?P<id>[\d]+)/(?P<value>[\d]+)/?$', 'ask.ajax.question_like'),
    url(r'^ajax/question_ask/?$', 'ask.ajax.question_ask'),
    url(r'^login/?$', 'ask.render.process_login'),
    url(r'^logout/?$', 'ask.render.process_logout'),
    url(r'^signup/?$', 'ask.render.signup'),
)
