from django.db.models import Model, CharField, SlugField, ImageField
from django.utils.text import slugify


class Category(Model):
    name = CharField(max_length=100, unique=True)
    slug = SlugField(unique=True)
    icon = CharField(max_length=255)

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        self.name = self.name.capitalize()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


