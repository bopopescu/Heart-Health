from django import forms
from registration.forms import RegistrationForm
from django.contrib.auth.models import User

class Email(forms.EmailField): 
    def clean(self, value):
        super(Email, self).clean(value)
        try:
            User.objects.get(email=value)
            raise forms.ValidationError("This email is already registered. If you have forgotten please use the 'forgot password' link on the login page.")
        except User.DoesNotExist:
            return value


class UserRegistrationForm(forms.Form):
    #email will be become username
    email = Email()

    email.label = 'Email Address:'
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password:")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm your password:")
    allow_notifications = forms.BooleanField(required=False, label="Allow email from Heart Health", initial=True)
    
    def clean_password(self):
        if self.data['password1'] != self.data['password2']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password1']

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        self.clean_password()
        return cleaned_data
