from django.conf.urls import patterns, include, url



urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^register/$', 'profiles.views.register', name="register"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name="logout"),
)
