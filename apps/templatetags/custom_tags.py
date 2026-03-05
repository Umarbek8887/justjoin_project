from django import template

register = template.Library()


@register.filter
def int_space(value):
    try:
        return f"{int(value):,}".replace(",", " ")
    except (ValueError, TypeError):
        return value
