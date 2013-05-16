from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import translation


def get_default_language():
    """
    Get the source language code if specified, or else just the default
    language code.
    """
    lang = getattr(settings, 'SOURCE_LANGUAGE_CODE', settings.LANGUAGE_CODE)
    default = [l[0] for l in settings.LANGUAGES if l[0] == lang]
    if len(default) == 0:
        # when not found, take first part ('en' instead of 'en-us')
        lang = lang.split('-')[0]
        default = [l[0] for l in settings.LANGUAGES if l[0] == lang]
    if len(default) == 0:
        raise ImproperlyConfigured(
            "The [SOURCE_]LANGUAGE_CODE '%s' is not found in your LANGUAGES "
            "setting." % lang)
    return default[0]


def get_current_language():
    """
    Get the current language
    """
    lang = translation.get_language()
    current = [l[0] for l in settings.LANGUAGES if l[0] == lang]
    if len(current) == 0:
        lang = lang.split('-')[0]
        current = [l[0] for l in settings.LANGUAGES if l[0] == lang]
    if len(current) == 0:
        # Fallback to default language code
        return get_default_language()

    return current[0]
