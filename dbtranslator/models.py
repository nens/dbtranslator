# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.db import models
# from django.utils.translation import ugettext_lazy as _


class MessageString(models.Model):
    """
    Message translation for the given language.
    
    """ 
    digest = models.CharField(max_length=40, db_index=True)
    language = models.CharField(max_length=5, db_index=True)
    message_id = models.TextField()
    message_str = models.TextField(blank=True)

    class Meta:
        unique_together = ('digest', 'language')

    def __unicode__(self):
        return '%s: %s (%s)' % (self.message_id, self.message_str, self.language)

