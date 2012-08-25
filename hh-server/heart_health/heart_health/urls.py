from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'survey.views.index', name='home'),
	url(r'^begin/', 'survey.views.begin', name='begin'),
    # Examples:
    # url(r'^$', 'heart_health.views.home', name='home'),
    # url(r'^heart_health/', include('heart_health.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
