from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models.enums import TextChoices
from django.db.models.fields import EmailField, BooleanField

from apps.managers import CustomUserManager


class User(AbstractUser):
    email = EmailField("email address", unique=True)
    is_active = BooleanField(default=False)
    username = None
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Roles(TextChoices):
        CANDIDATE = "candidate", "Candidate"
        EMPLOYER = "employer", "Employer"

    role = CharField(max_length=20, choices=Roles.choices)

    def is_candidate(self):
        return self.role == self.Roles.CANDIDATE

    def is_employer(self):
        return self.role == self.Roles.EMPLOYER

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


