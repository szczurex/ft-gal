from django.conf.urls import patterns, include, url



urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^register/$', 'profiles.views.register', name="register"),
    url(r'^register/success/$', 'profiles.views.register_success', name="register_success"),
    url(r'^register/activate/(?P<key>[0-9a-zA-Z\-]+)/$', 'profiles.views.register_activate', name="register_activate"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name="logout"),
)
