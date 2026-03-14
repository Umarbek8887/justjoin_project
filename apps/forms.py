import re

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import Form, CharField, ModelForm, EmailField

from apps.models import User, EmployerUser, CandidateUser
from apps.models.users import Roles


class LoginForm(Form):
    email = EmailField(required=True)
    password = CharField(max_length=128, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email or not password:
            return cleaned_data
        user = authenticate(email=email, password=password)

        if user is None:
            raise ValidationError("Incorrect email or password")

        if not user.is_active:
            raise ValidationError("Please activate your account")

        if not user.is_candidate():
            raise ValidationError("This account is not an candidate account")

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

    def save(self, commit = False):
        data = self.cleaned_data
        user = User.objects.create(
            email=data['email'],
            password=data['password'],
            role=Roles.CANDIDATE,
            is_active=False
        )
        return user



class EmployerRegisterForm(Form):
    email = EmailField(required=True)
    password = CharField(max_length=128, required=True)
    confirm_password = CharField(max_length=128, required=True)
    full_name = CharField(max_length=128, required=True)
    phone_number = CharField(max_length=20, required=True)
    country = CharField(max_length=128, required=True)

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise ValidationError("At least 8 characters.")

        if not re.search(r'[0-9]', password):
            raise ValidationError("At least one number.")

        if not re.search(r'[A-Z]', password):
            raise ValidationError("At least one uppercase letter.")

        if not re.search(r'[a-z]', password):
            raise ValidationError("At least one lowercase letter.")

        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            raise ValidationError("At least one special character.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if email:
            cleaned_data['email'] = email.lower()
            if User.objects.filter(email=cleaned_data['email']).exists():
                raise ValidationError("Email already exists")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords don't match")

        if password:
            cleaned_data['password'] = make_password(password)

        return cleaned_data

    def save(self):
        data = self.cleaned_data
        user = User.objects.create(
            email=data['email'],
            password=data['password'],
            role=Roles.EMPLOYER,
            first_name=data['full_name'].split()[0],
            last_name=data['full_name'].split()[1],
            is_active=False
        )
        EmployerUser.objects.create(
            user=user,
            phone_number=data['phone_number'],
            country=data['country'],
        )
        return user


class EmployerLoginForm(Form):
    email = EmailField(required=True)
    password = CharField(max_length=128, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if not email or not password:
            return cleaned_data

        user = authenticate(email=email, password=password)

        if user is None:
            raise ValidationError("Incorrect email or password")

        if not user.is_active:
            raise ValidationError("Please activate your account")

        if not user.is_employer():
            raise ValidationError("This account is not an employer account")

        self.user = user
        return cleaned_data



class UserBasicForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class CandidateProfileForm(ModelForm):
    class Meta:
        model = CandidateUser
        fields = [
            "image", "cv_file",
            "message_to_employee",
            "linkedin_link", "github_link", "other_link",
        ]



