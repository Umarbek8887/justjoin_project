from django.db.models import ImageField, PositiveSmallIntegerField, FileField, Model, ForeignKey, CASCADE, Q, \
    OneToOneField
from django.db.models.constraints import CheckConstraint
from django.db.models.enums import TextChoices
from django.db.models.fields import CharField, TextField

from apps.models import User


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


class LanguageLevel(TextChoices):
    I_KNOW_BASICS = "i know basics (a1, a2)", "I know basics (A1, A2)"
    I_CAN_WORK_WITH_IT_SOMETIMES = "i can work with it sometimes (b1, b2)", "I can work with it sometimes (B1, B2)"
    I_CAN_USE_IT_DAILY_AT_WORK = "i can use it daily at work (c1, c2)", "I can use it daily at work (C1, C2)"


class CandidateUser(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name="candidate_profile")
    github_link = CharField(max_length=255, null=True, blank=True)
    linkedin_link = CharField(max_length=255, null=True, blank=True)
    other_link = CharField(max_length=255, null=True, blank=True)
    message_to_employee = TextField(null=True)
    image = ImageField(upload_to='media/profile/avatar/%Y/%m/%d', null=True)
    current_position = CharField(max_length=128, null=True)
    years_of_exp = PositiveSmallIntegerField(default=0, db_default=0, null=True)
    location = CharField(max_length=128, null=True)
    native_lang = CharField(max_length=128, null=True)
    job_status = CharField(choices=SituationType.choices, max_length=64, default=SituationType.I_NEED_A_JOB_ASAP, null=True)
    availability_after = CharField(choices=AvailabilityAfter.choices, max_length=20,
                                   default=AvailabilityAfter.RIGHT_AWAY, null=True)
    cv_file = FileField(upload_to='media/cv/%Y/%m/%d', null=True, blank=True)

    class Meta:
        db_table = "apps_candidate_user"


class CandidateOtherPosition(Model):
    position = CharField(max_length=128, null=True)
    candidate_user = ForeignKey('apps.CandidateUser', CASCADE, related_name='candidate_other_positions')

    class Meta:
        verbose_name = 'Candidate Other Position'
        verbose_name_plural = 'Candidate Other Positions'
        db_table = "apps_candidate_user_other_positions"


class CandidateSkill(Model):
    tech_stack = CharField(max_length=128)
    level = PositiveSmallIntegerField(default=0, db_default=0)
    candidate_user = ForeignKey('apps.CandidateUser', CASCADE, related_name='candidate_skills')

    class Meta:
        verbose_name = 'Candidate Skill'
        verbose_name_plural = 'Candidate Skills'
        db_table = "apps_candidate_user_skills"
        constraints = [
            CheckConstraint(condition=Q(level__gte=0) & Q(level__lte=5),
                            name="level_gte_0_lte_5",
                            violation_error_message="Level must be between 0 and 5")
        ]


class CandidateLanguage(Model):
    language = CharField(max_length=128)
    language_level = CharField(choices=LanguageLevel.choices, max_length=128, default=LanguageLevel.I_KNOW_BASICS)
    candidate_user = ForeignKey('apps.CandidateUser', CASCADE, related_name='candidate_languagess')

    class Meta:
        db_table = "apps_candidate_user_languages"


