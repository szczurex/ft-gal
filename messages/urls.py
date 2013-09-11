from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'messages.views.index', name="index"),
)
