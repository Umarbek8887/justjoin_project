from django.db.models import Model, OneToOneField, CASCADE
from django.db.models.fields import CharField

from apps.models import User


class EmployerUser(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name="employer_profile")
    phone_number = CharField(max_length=20)
    country = CharField(max_length=128)

    class Meta:
        db_table = "apps_employer_user"
