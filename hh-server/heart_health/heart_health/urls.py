from django.conf.urls import patterns, include, url
from accounts.forms import UserRegistrationForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'survey.views.index', name='home'),
    url(r'^assess/basic/save/', 'survey.views.assess_basic_save', name='Save Basic'),
	url(r'^assess/basic/', 'survey.views.assess_basic', name='basic'),
    url(r'^assess/bio/save/', 'survey.views.assess_bio_save', name='Save Bio'),
	url(r'^assess/bio/', 'survey.views.assess_bio', name='Bio'),
    url(r'^assess/detail/save/', 'survey.views.assess_detail_save', name='Save Detail'),
	url(r'^assess/detail/', 'survey.views.assess_detail', name='Detail'),
	url(r'^locate/', 'survey.views.locate', name='Locate a Screening Center'),
	url(r'^results/get/', 'survey.views.get_results', name='Get Results'),
	url(r'^results/basic/', 'survey.views.results_basic', name='Basic Results'),
	url(r'^results/', 'survey.views.results', name='Results'),
    url(r'^register/$', 'registration.views.register',
            {
                'backend': 'accounts.regbackend.Backend',
                'form_class' : UserRegistrationForm
            },
            name='registration_register'
        ),
    url(r'^', include('registration.backends.default.urls')),

    # Examples:
    # url(r'^$', 'heart_health.views.home', name='home'),
    # url(r'^heart_health/', include('heart_health.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
