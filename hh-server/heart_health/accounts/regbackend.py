from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration import signals
from registration.forms import RegistrationForm
from registration.models import RegistrationProfile

from registration.backends import default


class Backend(default.DefaultBackend):
    def register(self, request, **kwargs):

        
        email, password = kwargs['email'], kwargs['password1']
        username = email
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(username, email, password, site)

        # if an anonymous user is registering, save their data
        if hasattr(request.user, 'userprofile'):
            if request.user.userprofile.is_anonymous:
                request.user.is_active = False
                request.user.save()
                survey = request.user.userprofile.survey
                survey.id = None
                survey.user_profile = new_user.userprofile
                survey.save()
                new_user.userprofile.survey = survey

        new_user.userprofile.allow_notifications = kwargs['allow_notifications']
        new_user.userprofile.save()

        signals.user_registered.send(sender=self.__class__,
                                                user=new_user,
                                                request=request)
        return new_user
  
