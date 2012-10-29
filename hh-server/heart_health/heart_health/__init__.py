from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from registration.signals import user_registered, user_activated

def login_on_registration_or_activation(sender, user, request, **kwargs):
    user.backend='django.contrib.auth.backends.ModelBackend' 
    login(request,user)
user_registered.connect(login_on_registration_or_activation)
user_activated.connect(login_on_registration_or_activation)

AuthenticationForm.base_fields['username'].max_length = 150
AuthenticationForm.base_fields['username'].widget.attrs['maxlength'] = 150
AuthenticationForm.base_fields['username'].validators[0].limit_value = 150
AuthenticationForm.base_fields['username'].label = "Email Address:"
