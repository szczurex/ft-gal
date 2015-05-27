from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^manage/submit/$', 'gallery.views.submit', name="submit"),
    url(r'^view/(?P<username>[0-9a-zA-Z\-]+)/$', 'gallery.views.index', name="index"),
    url(r'^view/(?P<username>[0-9a-zA-Z\-]+)/(?P<submission_id>[0-9]+)/$', 'gallery.views.view', name="view"),
)
