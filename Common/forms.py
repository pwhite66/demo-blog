from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = field.capitalize()


class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = field.capitalize()


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].icon_image = 'glyphicon-user'
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Username',
                                                                'autofocus': None})

        self.fields['password'].icon_image = 'glyphicon-lock'
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'Password'})


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Username',
                               }))
    username.icon_image = 'glyphicon-user'

    password = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Password'
                               }))
    password.icon_image = 'glyphicon-lock'

    confirm_password = forms.CharField(max_length=100,
                                       required=True,
                                       widget=forms.PasswordInput(attrs={
                                           'class': 'form-control',
                                           'placeholder': 'Confirm Password'
                                       }))
    confirm_password.icon_image = 'glyphicon-lock'

    name = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                               'placeholder': 'Name'
                           }))
    name.icon_image = 'glyphicon-user'

    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': 'Email',
                             }))
    email.icon_image = 'glyphicon-envelope'

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.user = None

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
            raise ValidationError('Error, Username already exists')
        except User.DoesNotExist:
            pass
        return username

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise ValidationError('Error, Passwords do not match')

        if 'username' in cleaned_data.keys():
            user = User()
            user.username = cleaned_data['username']
            user.set_password(cleaned_data['password'])
            user.first_name = cleaned_data['name']
            user.email = cleaned_data['email']
            user.save()
