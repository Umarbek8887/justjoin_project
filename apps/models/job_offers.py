from datetime import timedelta

from django.db.models import Model, CharField, TextChoices, ForeignKey, CASCADE, SlugField, Index, BooleanField, \
    PositiveIntegerField, PROTECT, ManyToManyField
from django.db.models.fields import DateTimeField
from django.utils.text import slugify
from django.utils.timezone import now
from django_ckeditor_5.fields import CKEditor5Field


class WorkingMode(TextChoices):
    REMOTE = "remote", "Remote"
    HYBRID = "hybrid", "hybrid"
    OFFICE = "office", "Office"


class ContractType(TextChoices):
    B2B = "b2b", "B2B"
    PERMANENT = "permanent", "Permanent"
    INTERNSHIP = "internship", "Internship"
    MANDATE_CONTRACT = "mandate contract", "Mandate contract"
    SPECIFIC_TASK_CONTRACT = "specific-task contract", "Specific-task contract"


class WorkingType(TextChoices):
    FULL_TIME = "full-time", "Full-time"
    PART_TIME = "part-time", "Part-time"
    FREELANCE = "freelance", "Freelance"
    PRACTICE_INTERNSHIP = "practice / internship", "Practice / Internship"


class Experience(TextChoices):
    JUNIOR = "junior", "Junior"
    MID = "mid", "Mid"
    SENIOR = "senior", "Senior"
    MANAGER_C_LEVEL = "manager / c-level", "Manager / C-level"


class LanguageLevel(TextChoices):
    A1 = "a1", "A1"
    A2 = "a2", "A2"
    B1 = "b1", "B1"
    B2 = "b2", "B2"
    C1 = "c1", "C1"
    C2 = "c2", "C2"


class TechStackLevel(TextChoices):
    NICE_TO_HAVE = "nice to have", "Nice to have"
    JUNIOR = "junior", "Junior"
    REGULAR = "regular", "Regular"
    ADVANCED = "advanced", "Advanced"
    MASTER = "master", "Master"


class SalaryType(TextChoices):
    HOURLY = "hourly", "Hourly"
    DAILY = "daily", "Daily"
    WEEKLY = "weekly", "Weekly"
    MONTHLY = "monthly", "Monthly"
    # YEARLY = "yearly", "Yearly"


class JobOffer(Model):
    name = CharField(max_length=255)
    description = CKEditor5Field(blank=True)
    slug = SlugField(max_length=255, unique=True, editable=False)

    working_mode = CharField(choices=WorkingMode.choices, max_length=32, default=WorkingMode.HYBRID)
    contract_type = CharField(choices=ContractType.choices, max_length=32, default=ContractType.INTERNSHIP)
    working_type = CharField(choices=WorkingType.choices, max_length=32, default=WorkingType.FULL_TIME)
    required_experience = CharField(choices=Experience.choices, max_length=32, default=Experience.JUNIOR)

    undisclosed_salary = BooleanField(default=False)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    published_at = DateTimeField()
    end_time = DateTimeField()
    is_active = BooleanField(default=True)

    languages = ManyToManyField('apps.Languages', through='JobLanguage', related_name='jobs')
    tech_stacks = ManyToManyField('apps.TechStack', through='JobTechStack', related_name='jobs')
    company = ForeignKey('apps.Company', on_delete=CASCADE, related_name='job_offers')
    category = ForeignKey('apps.Category', on_delete=CASCADE, related_name='job_offers')

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = self.name.title()
        self.slug = slugify(
            f"{self.company.slug}-{self.name}-{self.company.location_name}-{self.category.name}-{self.pk}")
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    class Meta:
        indexes = [
            Index(fields=["working_mode"]),
            Index(fields=["working_type"]),
            Index(fields=["required_experience"]),
            Index(fields=["contract_type"])
        ]

    @property
    def is_new(self):
        return self.created_at > now() - timedelta(days=2)

    @property
    def image(self):
        return self.company.image

    @property
    def left_days(self) -> int:
        delta = self.end_time - self.published_at
        return delta.days


class JobLanguage(Model):
    job_offer = ForeignKey('apps.JobOffer', on_delete=CASCADE, related_name='job_languages')
    language = ForeignKey('apps.Languages', on_delete=CASCADE, related_name='language_jobs')
    level = CharField(choices=LanguageLevel.choices, max_length=2, default=LanguageLevel.A1)

    class Meta:
        unique_together = ('job_offer', 'language')


class JobTechStack(Model):
    job_offer = ForeignKey('apps.JobOffer', on_delete=CASCADE, related_name='job_tech_stack')
    tech_stack = ForeignKey('apps.TechStack', on_delete=CASCADE, related_name='tech_jobs')
    level = CharField(choices=TechStackLevel.choices, max_length=20, default=TechStackLevel.JUNIOR)

    class Meta:
        unique_together = ('job_offer', 'tech_stack')


class Languages(Model):
    name = CharField(max_length=128)

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = self.name.capitalize()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class TechStack(Model):
    name = CharField(max_length=128)

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = self.name.capitalize()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class Currency(Model):
    name = CharField(max_length=64)
    iso = CharField(max_length=8, unique=True)

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.iso = self.iso.upper()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class Salary(Model):
    salary_min = PositiveIntegerField(null=True, blank=True)
    salary_max = PositiveIntegerField(null=True, blank=True)
    salary_type = CharField(choices=SalaryType.choices, max_length=12, default=SalaryType.MONTHLY)
    currency = ForeignKey('apps.Currency', on_delete=PROTECT, related_name='salaries')
    job_offer = ForeignKey('apps.JobOffer', on_delete=CASCADE, related_name='salaries')

    @property
    def currency_iso(self):
        return self.currency.iso
