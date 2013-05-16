# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.core.management.base import BaseCommand

from dbtranslator.models import MessageString


class Command(BaseCommand):
    help = 'Update the database catalog with translation source files.'

    def handle(self, *args, **options):
        from dbtranslator import REGISTRY
        for model in REGISTRY:
            print(model, REGISTRY[model])
        else:
            print("No model fields registered for translation.")
