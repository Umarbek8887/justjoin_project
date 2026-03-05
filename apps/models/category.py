from django.db.models import Model, CharField, SlugField, FileField
from django.utils.text import slugify


class Category(Model):
    name = CharField(max_length=100, unique=True)
    slug = SlugField(unique=True, editable=False)
    svg = FileField(upload_to=f'category/svg/')

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        self.name = self.name.capitalize()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return self.name

    @property
    def active_jobs_count(self):
        return self.job_offers.filter(is_active=True).count()

    class Meta:
        verbose_name_plural = 'Categories'
