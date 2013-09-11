from django.conf.urls import patterns, include, url

# NOTE: the order matters here.

urlpatterns = patterns('',
    url(r'^mine/$', 'journals.views.mine', name="mine"),
    url(r'^edit/$', 'journals.views.edit', name="edit"),
    url(r'^edit/(?P<id>[\d]+)/$', 'journals.views.edit', name="edit"),
    url(r'^delete/(?P<id>[\d]+)/$', 'journals.views.delete', name="delete"),
    url(r'^(?P<username>[0-9a-zA-Z\-]+)/$', 'journals.views.index', name="index"),
)
