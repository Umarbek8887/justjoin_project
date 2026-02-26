from django.db.models import Model, CharField, TextChoices, ForeignKey, CASCADE, FloatField, SlugField, Index, \
    PositiveIntegerField, Q, F, BooleanField
from django.db.models.constraints import CheckConstraint
from django.utils.timezone import now
from django.db.models.fields import DateTimeField
from django.utils.text import slugify
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
    programming_language = CharField(max_length=128)
    slug = SlugField(max_length=255, blank=True, unique=True)
    updated_at = DateTimeField(auto_now_add=True)
    created_at = DateTimeField(auto_now=True)
    end_time = DateTimeField()
    is_active = BooleanField(default=True)

    working_mode = CharField(choices=WorkingMode.choices, max_length=32, default=WorkingMode.HYBRID)
    contract_type = CharField(choices=ContractType.choices, max_length=32, default=ContractType.INTERNSHIP)
    working_type = CharField(choices=WorkingType.choices, max_length=32, default=WorkingType.FULL_TIME)
    required_experience = CharField(choices=Experience.choices, max_length=32, default=Experience.JUNIOR)
    salary_type = CharField(choices=SalaryType.choices, max_length=12, default=SalaryType.MONTHLY)

    undisclosed_salary = BooleanField(default=False)
    salary_min = PositiveIntegerField(null=True, blank=True)
    salary_max = PositiveIntegerField(null=True, blank=True)

    currency = CharField(max_length=10, default="USD")

    location = CharField(max_length=255)
    lat = FloatField(blank=True, null=True)
    long = FloatField(blank=True, null=True)

    company = ForeignKey('apps.Company', on_delete=CASCADE, related_name='job_offers')

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(f"{self.company.slug}-{self.name}-{self.company.location_name}-{self.programming_language}")
        if not self.location:
            self.location = self.company.location_name
            self.lat = self.company.lat
            self.long = self.company.long
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    class Meta:
        indexes = [
            Index(fields=["slug"]),
            Index(fields=["working_mode"]),
            Index(fields=["main_language"]),
            Index(fields=["working_type"]),
            Index(fields=["required_experience"]),
            Index(fields=["contract_type"])
        ]
        # constraints = [
        #     CheckConstraint(
        #         check=Q(salary_min__lte=F("salary_max")),
        #         name="salary_min_lte_salary_max"
        #     )
        # ]
    @property
    def is_new(self):
        return self.created_at > now().replace(hour=0, minute=0, second=0)

    @property
    def image(self):
        return self.company.image



class OfferLanguages(Model):
    language = CharField(max_length=128)
    level = CharField(choices=LanguageLevel.choices, max_length=4, default=LanguageLevel.A1)
    job_offer = ForeignKey('apps.JobOffer', on_delete=CASCADE, related_name='languages')


class OfferRequirements(Model):
    tech_stack = CharField(max_length=128)
    level = CharField(choices=TechStackLevel.choices, max_length=16, default=TechStackLevel.NICE_TO_HAVE)
    job_offer = ForeignKey('apps.JobOffer', on_delete=CASCADE, related_name='requirements')
