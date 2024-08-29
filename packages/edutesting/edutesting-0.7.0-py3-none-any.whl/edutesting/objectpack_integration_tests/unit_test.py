# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals

from django.db.models.fields import AutoField
from django.conf import settings

from m3.actions import _import_by_path

from .base_test import BaseTest
import six


path = getattr(settings, 'OBJECTPACK_BASE_TEST', None)
if path:
    patched_base_test = _import_by_path(path)
else:
    patched_base_test = BaseTest


class BaseUnitTestModel(patched_base_test):
    exclude_field_checker = ['lft', 'rght', 'tree_id', 'level', ]
    exclude_model_checker = []
    testing_model = None

    def test_spell_model_verbose_name(self):
        """
        Проверка орфографии verbose_name в моделях
        """
        model = self.testing_model
        if model and model.__name__ not in self.exclude_model_checker:
            verbose_name = model._meta.verbose_name
            self.assertTrue(self.check_spell(six.text_type(verbose_name)),
                            verbose_name)

    def test_have_model_verbose_name(self):
        """
        Проверка наличия в классе Meta модели verbose_name
        """
        model = self.testing_model
        if model and model.__name__ not in self.exclude_model_checker:
            model_name = model.__name__.lower()
            verbose_name = six.text_type(model._meta.verbose_name)
            is_equal = model_name != verbose_name
            self.assertTrue(
                is_equal,
                'Model used default class name in verbose name.')

    def test_have_model_verbose_name_plural(self):
        """
        Проверка наличия в классе Meta модели verbose_name_plural
        """
        model = self.testing_model
        if model and model.__name__ not in self.exclude_model_checker:
            model_name = model.__name__.lower()
            verbose_name_plural = model._meta.verbose_name_plural
            is_equal = model_name != verbose_name_plural + u's'
            self.assertTrue(
                is_equal,
                'Model used default class name in verbose name.')

    def test_have_model_fields_verbose_name(self):
        """
        Проверка наличия в field модели verbose_name
        """
        model = self.testing_model
        if model and model.__name__ not in self.exclude_model_checker:
            all_fields = model._meta.fields
            res = []
            for temp_field in all_fields:
                if temp_field.name not in self.exclude_field_checker:
                    if not isinstance(temp_field, AutoField):
                        if not temp_field.name.endswith('_ptr'):
                            verbose_name = six.text_type(temp_field.verbose_name)
                            field_name = temp_field.name.replace('_', ' ')
                            if not verbose_name != field_name:
                                res.append((field_name, str(model)))
            self.assertFalse(
                res, "Fields don't have verbose name: {}".format(res))

    def test_spell_model_fields_verbose_name(self):
        """
        Проверка орфографии у полей модели
        """
        model = self.testing_model
        if model and model.__name__ not in self.exclude_model_checker:
            all_fields = model._meta.fields
            res = []
            for field in all_fields:
                if field.name not in self.exclude_field_checker:
                    if not isinstance(field, AutoField):
                        if not field.name.endswith('_ptr'):
                            verbose_name = six.text_type(field.verbose_name)
                            if not self.check_spell(verbose_name):
                                res.append((verbose_name, field))
                    if hasattr(field, 'choices') and field.choices:
                        for key, val in field.choices:
                            if not self.check_spell(val):
                                res.append((val, field))
            self.assertFalse(res, 'Bad spelling: {}'.format(res))
