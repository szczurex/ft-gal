from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ft.views.home', name='home'),
    # url(r'^ft/', include('ft.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profiles/', include('profiles.urls', namespace="profiles")),
    url(r'^favourites/', include('favourites.urls', namespace="favourites")),
    url(r'^gallery/', include('gallery.urls', namespace="gallery")),
    url(r'^journals/', include('journals.urls', namespace="journals")),
    url(r'^messages/', include('msg.urls', namespace="messages")),
    url(r'^', include('main.urls', namespace="main")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
