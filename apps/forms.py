import re

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import Form, CharField, ModelForm, EmailField

from apps.models import User


class LoginForm(Form):
    email = EmailField(required=True)
    password = CharField(max_length=128, required=True)

    def clean(self):
        cleaned_data = super().clean()

        user = authenticate(**cleaned_data)
        if user is None:
            raise ValidationError("Incorrect username or password")

        self.user = user
        return cleaned_data


class RegisterModelForm(ModelForm):
    confirm_password = CharField(max_length=255, required=True)
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = 'email', 'password'

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if len(password) < 8:
            raise ValidationError("At least 8 characters.")

        if not re.search(r'[0-9]', password):
            raise ValidationError("At least one number.")

        if not re.search(r'[A-Z]', password):
            raise ValidationError("At least one uppercase letter.")

        if not re.search(r'[a-z]', password):
            raise ValidationError("At least one lowercase letter.")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("At least one special character.")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords don't match")

        return password

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email:
            cleaned_data['email'] = email.lower()
            if User.objects.filter(email=cleaned_data['email']).exists():
                raise ValidationError("Email already exists")

        if password:
            cleaned_data['password'] = make_password(password)

        return cleaned_data
