from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^view/(?P<username>[0-9a-zA-Z\-]+)/$', 'favourites.views.index', name="index"),
)
