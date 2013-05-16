# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.db import models
from django.utils.datastructures import SortedDict

from dbtranslator.models import MessageString
from dbtranslator.utils import get_current_language, get_default_language

REGISTRY = SortedDict()


def _dbtranslator_pre_save(sender, instance, **kwargs):
    setattr(instance, '_dbtranslator_saving', True)


def _dbtranslator_post_save(sender, instance, **kwargs):
    delattr(instance, '_dbtranslator_saving')


def register(model, fields):
    """Tell dbtranslator which fields on a Django model should be translated.

    Arguments:
    model -- The model class
    fields -- A list or tuple of field names. e.g. ['name', 'nickname']

    """
    if not model in REGISTRY:
        # create a fields dict (models apparently lack this?!)
        fields = dict([(f.name, f) for f in model._meta._fields() if f.name in
                       fields])

        REGISTRY[model] = fields

        models.signals.pre_save.connect(_dbtranslator_pre_save, sender=model)
        models.signals.post_save.connect(_dbtranslator_post_save, sender=model)

        for field in fields.values():
            setattr(model, field.name, FieldDescriptor(field.name))


class FieldDescriptor(object):
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        language = get_current_language()
        msg_id = instance.__dict__[self.name]
        if not msg_id:
            return u''
        if instance.id is None:
            return msg_id
        return MessageString.objects.lookup(msg_id, language)

    def __set__(self, instance, value):
        lang_code = get_current_language()
        default_lang = get_default_language()

        if (lang_code == default_lang or not self.name in instance.__dict__ or
                instance.id is None):
            instance.__dict__[self.name] = value
        else:
            original = instance.__dict__[self.name]
            if original == u'':
                instance.__dict__[self.name] = value
                original = value

            message_string = MessageString.objects.get_msg_str(original,
                                                               lang_code)
            message_string.msg_str = value
            message_string.save()

        return None
