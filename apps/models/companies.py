from django.db.models import Model, ImageField, TextChoices
from django.db.models.fields import CharField
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
    banner = ImageField(upload_to='media/company/banner/%Y/%m/%d')
    image = ImageField(upload_to='media/company/avatar/%Y/%m/%d')
    company_type = CharField(choices=CompanyType.choices, max_length=64, default=CompanyType.OTHER)
    industry = CharField(max_length=64)
