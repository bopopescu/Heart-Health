from django.contrib.auth.forms import AuthenticationForm

AuthenticationForm.base_fields['username'].max_length = 150
AuthenticationForm.base_fields['username'].widget.attrs['maxlength'] = 150
AuthenticationForm.base_fields['username'].validators[0].limit_value = 150
AuthenticationForm.base_fields['username'].label = "Email Address"
