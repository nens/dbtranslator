# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from hashlib import sha1

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models import signals
from django.db.models.query import QuerySet


def make_digest(key):
    """Get the SHA1 hexdigest of the given key"""
    return sha1(key.encode('utf-8')).hexdigest()


def _get_cache_keys(self):
    """Get all the cache keys for the given object"""
    kv_id_fields = ('language', 'digest')
    values = tuple(getattr(self, attr) for attr in kv_id_fields)
    return ('dbtranslator_%s_%s' % values,
            'dbtranslator_%s' % self.id)


CACHE_DURATION = getattr(settings, 'DBTRANSLATOR_CACHE_DURATION', 60 * 60)


class MessageStringManager(models.Manager):
    def get_query_set(self):
        return MessageStringQuerySet(self.model)

    def get_msg_str(self, msg_id, language):
        msg_id = msg_id or ''
        digest = make_digest(msg_id)
        message_string, created = self.get_or_create(
            digest=digest, language=language, message_id=msg_id)
        return message_string

    def lookup(self, msg_id, language):
        message_string = self.get_msg_str(msg_id, language)
        if message_string.msg_str:
            return message_string.msg_str
        else:
            return msg_id

    def contribute_to_class(self, model, name):
        signals.post_save.connect(self._post_save, sender=model)
        signals.post_delete.connect(self._post_delete, sender=model)
        setattr(model, '_get_cache_keys', _get_cache_keys)
        setattr(model, 'cache_keys', property(_get_cache_keys))
        return super(MessageStringManager, self).contribute_to_class(model,
                                                                     name)

    def _invalidate_cache(self, instance):
        """
        Explicitly set a None value instead of just deleting so we don't have
        any race conditions where.
        """
        for key in instance.cache_keys:
            cache.set(key, None, 5)

    def _post_save(self, instance, **kwargs):
        """
        Refresh the cache when saving.
        """
        for key in instance.cache_keys:
            cache.set(key, instance, CACHE_DURATION)

    def _post_delete(self, instance, **kwargs):
        self._invalidate_cache(instance)


class MessageStringQuerySet(QuerySet):
    def iterator(self):
        superiter = super(MessageStringQuerySet, self).iterator()
        while True:
            obj = superiter.next()
            # Use cache.add instead of cache.set to prevent race conditions
            for key in obj.cache_keys:
                cache.add(key, obj, CACHE_DURATION)
            yield obj

    def get(self, *args, **kwargs):
        """
        Checks the cache to see if there's a cached entry for this pk. If not,
        fetches using super then stores the result in cache.

        Most of the logic here was gathered from a careful reading of
        ``django.db.models.sql.query.add_filter``
        """
        if self.query.where:
            # If there is any other ``where`` filter on this QuerySet just call
            # super. There will be a where clause if this QuerySet has already
            # been filtered/cloned.
            return super(MessageStringQuerySet, self).get(*args, **kwargs)

        kv_id_fields = ('language', 'digest')

        # Punt on anything more complicated than get by pk/id only...
        if len(kwargs) == 1:
            k = kwargs.keys()[0]
            if k in ('pk', 'pk__exact', 'id', 'id__exact'):
                obj = cache.get('dbtranslator_%s' % kwargs.values()[0])
                if obj is not None:
                    return obj
        elif set(kv_id_fields) <= set(kwargs.keys()):
            values = tuple(kwargs[attr] for attr in kv_id_fields)
            obj = cache.get('dbtranslator_%s_%s' % values)

            if obj is not None:
                return obj

        # Calls self.iterator to fetch objects, storing object in cache.
        return super(MessageStringQuerySet, self).get(*args, **kwargs)


class MessageString(models.Model):
    """
    Message translation for the given language.

    """
    digest = models.CharField(max_length=40, db_index=True)
    language = models.CharField(max_length=5, db_index=True)
    message_id = models.TextField()
    message_str = models.TextField(blank=True)

    objects = MessageStringManager()

    class Meta:
        unique_together = ('digest', 'language')

    def __unicode__(self):
        return '%s: %s (%s)' % (self.message_id, self.message_str,
                                self.language)
