from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^view/(?P<username>[0-9a-zA-Z\-]+)/$', 'favourites.views.index', name="index"),
    url(r'^add/(?P<username>[0-9a-zA-Z\-]+)/(?P<submission_id>[0-9]+)/$', 'favourites.views.add', name="add"),
)
