from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField, PositiveSmallIntegerField, BooleanField
from django.db.models.enums import TextChoices
from django.db.models.fields import CharField, TextField, EmailField

from apps.managers import CustomUserManager


class CandidateUser(AbstractUser):
    email = EmailField("email address", unique=True)
    is_active = BooleanField(default=False)
    username = None
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



    class SituationType(TextChoices):
        I_NEED_A_JOB_ASAP = "i need a job asap", "I need a job ASAP"
        I_AM_OPEN_TO_OFFERS = "i'm open to offers", "I'm open to offers"
        I_AM_LOOKING_FOR_A_NEW_JOB_NOW = "i'm not looking for a new job now", "I'm not looking for a new job now"


    class AvailabilityAfter(TextChoices):
        RIGHT_AWAY = "right away", "Right away"
        IN_1_WEEK = "in 1 week", "In 1 week"
        IN_2_WEEKS = "in 2 weeks", "In 2 weeks"
        IN_ABOUT_A_MONTH = "in about a month", "In about a month"
        IN_2_MONTHS = "in 2 months", "In 2 months"
        IN_3_MONTHS = "in 3 months", "In 3 months"

    # class JobPosition(TextChoices):
    #     USER = 'user', 'User'
    #     ADMIN = 'admin', 'Admin'

    github_link = CharField(max_length=255, null=True, blank=True)
    linkedin_link = CharField(max_length=255, null=True, blank=True)
    other_link = CharField(max_length=255, null=True, blank=True)
    message_to_employee = TextField(null=True)
    image = ImageField(upload_to='media/profile-avatar/%Y/%m/%d')
    # current_position = CharField(choices=JobPosition.choices, max_length=20, default=JobPosition.USER)
    years_of_exp = PositiveSmallIntegerField(default=0, db_default=0)
    location = CharField(max_length=128, null=True)
    native_lang = CharField(max_length=128, null=True)
    job_status = CharField(choices=SituationType.choices, max_length=20, default=SituationType.I_NEED_A_JOB_ASAP)
    availability_after = CharField(choices=AvailabilityAfter.choices, max_length=20, default=AvailabilityAfter.RIGHT_AWAY)





