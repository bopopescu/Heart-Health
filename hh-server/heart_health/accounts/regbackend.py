from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from registration import signals
from registration.forms import RegistrationForm
from registration.models import RegistrationProfile
from survey.models import Survey

from registration.backends import default


class Backend(default.DefaultBackend):
    def register(self, request, **kwargs):
        email, password = kwargs['email'], kwargs['password1']
        username = email
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = HtmlRegistrationProfile.objects.create_inactive_user(username, email, password, site)
        new_user.userprofile.survey = Survey()

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

        new_user.userprofile.survey.save()
        new_user.userprofile.allow_notifications = kwargs['allow_notifications']
        new_user.userprofile.save()

        signals.user_registered.send(sender=self.__class__,
                                                user=new_user,
                                                request=request)
        return new_user
  
class HtmlRegistrationProfile(RegistrationProfile):
    class Meta:
        proxy = True
    def send_activation_email(self, site):
        """Send the activation mail"""
        
        ctx_dict = {'activation_key': self.activation_key,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                    'site': site}
        subject = render_to_string('registration/activation_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message_text = render_to_string('registration/activation_email.txt', ctx_dict)
        message_html = render_to_string('registration/activation_email.html', ctx_dict)

        msg = EmailMultiAlternatives(subject, message_text, settings.DEFAULT_FROM_EMAIL, [self.user.email])
        msg.attach_alternative(message_html, "text/html")
        msg.send()
