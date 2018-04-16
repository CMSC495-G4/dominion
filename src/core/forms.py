from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

def custom_attrs(field):
  return {
    'class': 'form-control',
    'data-html': 'true',
    'data-placement': 'top',
    'data-toggle': 'tooltip',
    'title': field.help_text,
    'placeholder': field.label,
  }

class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in self.Meta.fields:
            field = self.fields[key]
            field.widget.attrs = custom_attrs(field)

class SignupForm(UserCreationForm):

    email = forms.EmailField(
      max_length=254,
      help_text='Required. Please enter a valid email address.',
      label='Email'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in self.Meta.fields:
            field = self.fields[key]
            field.widget.attrs = custom_attrs(field)