from django.db.models import Model, ImageField, TextChoices, FloatField, ForeignKey, CASCADE, PositiveSmallIntegerField, \
    PositiveIntegerField, SlugField
from django.db.models.fields import CharField
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class CompanyType(TextChoices):
    STARTUP = "startup", "Startup"
    CORPORATION = "corporation", "Corporation"
    SOFTWARE_HOUSE = "software house", "Software House"
    AGENCY = "agency", "Agency"
    E_COMMERCE = "e-commerce", "E-commerce"
    OTHER = "other", "Other"


class Company(Model):
    name = CharField(max_length=255)
    description = CKEditor5Field(blank=True)
    banner = ImageField(upload_to='company/banner/')
    image = ImageField(upload_to='company/avatar/')
    slug = SlugField(max_length=255, blank=True, unique=True, editable=False)
    company_type = CharField(choices=CompanyType.choices, max_length=64, default=CompanyType.OTHER)
    industry = CharField(max_length=64, blank=True)
    founded = PositiveSmallIntegerField()
    origin = CharField(max_length=255)
    number_of_employees = PositiveIntegerField(null=True, blank=True)
    x_link = CharField(max_length=255, null=True, blank=True)
    web_site = CharField(max_length=255, null=True, blank=True)
    facebook_link = CharField(max_length=255, null=True, blank=True)
    linkedin_link = CharField(max_length=255, null=True, blank=True)
    instagram_link = CharField(max_length=255, null=True, blank=True)
    youtube_link = CharField(max_length=255, null=True, blank=True)
    tiktok_link = CharField(max_length=255, null=True, blank=True)
    employer_user = ForeignKey('apps.EmployerUser', on_delete=CASCADE, related_name='companies')

    location_name = CharField(max_length=255, blank=True)
    lat = FloatField(blank=True, null=True)
    long = FloatField(blank=True, null=True)

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'

class CompanyOtherLocations(Model):
    location_name = CharField(max_length=128)
    lat = FloatField()
    long = FloatField()
    company = ForeignKey('apps.Company', on_delete=CASCADE, related_name='company_locations')
