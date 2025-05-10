from django import forms
from django.contrib.auth.forms import UserChangeForm as DefaultUserChangeForm
from django.contrib.auth.forms import \
    UserCreationForm as DefaultUserCreationForm
from django.core.exceptions import ValidationError

from .models import Client, User


class UserCreationForm(DefaultUserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class UserChangeForm(DefaultUserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirm Password'
    )

    class Meta:
        model = Client
        fields = ('first_name', 'last_name')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            print('ERROR!!!!!!!')
            raise ValidationError('Password do not match', code=400)

        return cleaned_data
