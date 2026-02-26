from django.contrib.auth import authenticate
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import Form, CharField, ModelForm, EmailField

from apps.models import User



class LoginForm(Form):
    username = UsernameField(required=True)
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


    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if email:
            cleaned_data['email'] = email.lower()
            if User.objects.filter(email=cleaned_data['email']).exists():
                raise ValidationError("Email already exists")

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords don't match")

        if password:
            cleaned_data['password'] = make_password(password)

        return cleaned_data



