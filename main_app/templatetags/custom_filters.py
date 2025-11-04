"""
Custom template filters for Django 5.x compatibility.

This module provides custom template filters that restore functionality
removed in Django 5.0+, ensuring compatibility with third-party packages
like django-jazzmin that still rely on deprecated filters.
"""

from django import template

register = template.Library()


@register.filter(name='length_is')
def length_is(value, arg):
    """
    Returns True if the length of the value is equal to the argument.
    This filter was removed in Django 5.0 but is still used by Jazzmin templates.

    Usage: {% if mylist|length_is:"3" %}
    """
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return False
