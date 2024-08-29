# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import copy
import datetime
import os.path
import random
import re
import string

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from m3_ext.ui.fields.base import BaseExtField
from m3_ext.ui.fields.complex import ExtFileUploadField
from m3_ext.ui.fields.complex import ExtImageUploadField
from m3_ext.ui.fields.simple import ExtCheckBox
from m3_ext.ui.fields.simple import ExtDateField
from m3_ext.ui.fields.simple import ExtDateTimeField
from m3_ext.ui.fields.simple import ExtHTMLEditor
from m3_ext.ui.fields.simple import ExtNumberField
from m3_ext.ui.fields.simple import ExtStringField
from m3_ext.ui.fields.simple import ExtTextArea
from objectpack.models import VirtualModel, ModelProxy
from objectpack.tools import int_or_zero
from objectpack.tools import str_to_date
from objectpack.ui import WindowTab, TabbedEditWindow, BaseEditWindow
import six
from six.moves import range
from six.moves import zip


CONTEXT_PARAMS_TYPES = {
    'date_types': (
        'date',
        'str_to_date',
        'date_or_none',
        str_to_date,
    ),
    'int_types': (
        int,
        'int',
        int_or_zero,
        'int_or_zero',
        'int_or_none',
    ),
    'json': (
        'json',
    ),
    'str_types': (
        'str',
        'unicode',
        six.text_type,
        str,
        'str_or_none',
    )
}


def get_meta_for_model(model):
    """
    Возвращает meta структуру для модели

    :param model: модель, для которой необходимо вернуть meta
    :return: meta структура
    """
    if VirtualModel in model.__mro__ or ModelProxy in model.__mro__:
        return model.model._meta
    return model._meta


def get_obj_by_id(obj_model, obj_id):
    """
    Возвращает объект заданной модели по id или None
    :param obj_model
    :type obj_model: django.db.model
    :param obj_id:
    :type obj_id: int
    :return: object
    """
    try:
        return obj_model.objects.get(id=int(obj_id))
    except (AttributeError, ObjectDoesNotExist):
        return None


def parse_to_filter(orig_filter):
    """
    Переворачиваем дату от пользователя

    :param orig_filter: подготовительный словарь для будущей записи в БД,
        ключи - имена полей модели model,
        значения - значения для полей
    :type orig_filter: dict
    :return: подготовительный словарь для будущей записи в БД,
        ключи - имена полей модели model,
        значения - значения для полей
    :rtype: dict
    """
    temp_filter = dict(list(zip(list(orig_filter.keys()), list(orig_filter.values()))))
    for k in temp_filter.keys():
        re_match = re.match(
            r'^(\d\d)\.(\d\d)\.(\d\d\d\d)$',
            '%s' % temp_filter[k]
        )
        if re_match:
            temp_filter[k] = '-'.join(re_match.groups()[::-1])
    return temp_filter


def generate_good_uniq(temp_filter, model, condition):
    """
    :param temp_filter: подготовительный словарь для будущей записи в БД,
        ключи - имена полей модели model,
        значения - значения для полей
    :type temp_filter: dict
    :param model: модель, для которой проверяем запись на уникальность
    :type model: django.db.model
    :param condition: условия, по которым будем генеририровать даныне,
        в случае нарушения уникальности
    :type condition: dict
    :return: подготовительный словарь для будущей записи в БД,
        ключи - имена полей модели model,
        значения - значения для полей
    :rtype: dict
    """
    last_fk = None
    last_key = None

    for key in temp_filter.keys():
        field_name = key[0:-3] if key.endswith('_id') else key
        temp_field = get_meta_for_model(model).get_field_by_name(field_name)[0]

        if (isinstance(temp_field, models.ForeignKey) and
                temp_field.rel.to not in list(condition.keys())):

            last_fk = temp_field
            last_key = key
            id_list = temp_field.rel.to.objects.exclude(
                id=temp_filter[key]
            ).values_list('id', flat=True)
            for temp_id in id_list:
                if not model.objects.filter(**parse_to_filter(
                        temp_filter)).exists():
                    temp_filter[key] = temp_id
                    return temp_filter

    if last_fk and last_key:
        temp_filter[last_key] = GM(last_fk.rel.to, condition).get().id

    return temp_filter


def gen_uniq(params, model, condition):
    """
    :param params: подготовительный словарь для будущей записи в БД,
        ключи - имена полей модели model,
        значения - значения для полей
    :type params: dict
    :param model: модель, для которой проверяем запись на уникальность
    :type model: django.db.model
    :param condition: условия, по которым будем генеририровать даныне,
        в случае нарушения уникальности
    :type condition: dict
    :return: подготовительный словарь для будущей записи в БД,
        ключи - имена полей модели model,
        значения - значения для полей
    :rtype: dict
    """
    uniq_list = list(get_meta_for_model(model).unique_together)

    for i in get_meta_for_model(model).fields:
        if isinstance(i, models.OneToOneField) or\
                (isinstance(i, models.ForeignKey) and i.unique):
            uniq_list.append((i.name, ))

    if not uniq_list:
        return params

    for uniq_tuple in uniq_list:
        temp_filter = {}
        for key in params.keys():
            for uniq in uniq_tuple:
                if key.endswith('_id'):
                    uniq = '_'.join([uniq, 'id'])
                if uniq == key and temp_filter.get(key, -1) == -1:
                    temp_filter[key] = params[key]

        if temp_filter:
            f_names = [i.name for i in get_meta_for_model(model).fields]
            no_model_fields = [
                i
                for i in temp_filter.keys()
                if (i not in f_names and 'id' not in i)
            ]
            for i in no_model_fields:
                del temp_filter[i]

            if model.objects.filter(**parse_to_filter(temp_filter)).exists():
                uniq_filter = generate_good_uniq(temp_filter, model, condition)
                for i in uniq_filter.keys():
                    params[i] = uniq_filter[i]

    return params


class PackValueForContext(object):
    """
    Класс для поиска и генерации значений
    (либо берем из БД, либо создаем свой)
    по записям declare_context
    """
    def __init__(self, key, val, condition, gm=False):
        """
        Инициализация созданного объекта

        :param key: имя параметра, для которого необходимо
            сгенерировать/найти данные
        :param val: type of key
        :param condition: условия, по которым ищем или генерируем данные
        :type condition: dict
        :param gm: gm=True, генерируем, в противном случае - нет
        :type gm: bool
        """
        self.key = key  # название св-ва, как правило это id_param_name
        self.val = val  # описание св-ва {'type': int}
        self.condition = copy.copy(condition)  # словарь условий, {Model: id}
        self.gm = gm  # Если не нашли в БД, генерируем, по умолчанию нет

    def get(self):
        """
        Основной метод для получения необхдимого значения контекста
        """

        if self.val['type'] in CONTEXT_PARAMS_TYPES['str_types']:
            if 'date' in self.key:
                return datetime.datetime.now().strftime("%d.%m.%Y")
            else:
                return GM.str_generator(5)

        if self.val['type'] in CONTEXT_PARAMS_TYPES['date_types']:
            val = datetime.datetime.now()
            delta = datetime.timedelta(days=5)

            if 'begin' in self.key or 'from' in self.key:
                val -= delta

            if 'end' in self.key or 'to 'in self.key:
                val += delta

            return val.strftime("%d.%m.%Y")

        if self.val['type'] == 'json':
            return '[]'

        if self.val['type'] == 'time':
            return datetime.time(1, 1)

        id_match = re.compile('.*(?P<id>(id))$')
        res = id_match.match(self.key)
        if res and res.group('id') == 'id':
            return self.find_value_from_db()

        if self.key == 'ids' or self.val['type'] == 'int_list':
            return [0]

        if self.val['type'] in CONTEXT_PARAMS_TYPES['int_types']:
            return random.randint(1, 1000)

    def find_value_from_db(self):
        """
        Среди зарегистррованных паков ищем тот,
        у которого id_param_name свопадает с искомым ключом.
        В найденном паке берем модель и достаем объект из нее (или генерим)
        """
        from .integration_test import PATCHED_BASE_INTEGRATION_TEST
        pack_list = PATCHED_BASE_INTEGRATION_TEST.get_list_pack_from_observer()
        for pack in pack_list:
            if hasattr(pack, 'model') and hasattr(pack, 'id_param_name'):
                primary_for_model = getattr(
                    pack, '_is_primary_for_model', False
                )
                if pack.id_param_name == self.key and (
                        self.key.count('.') > 2 or
                        primary_for_model
                ):
                    modelcls = pack.model
                    if VirtualModel in modelcls.__mro__:
                        modelcls = modelcls.model

                    filter_cond, exclude_cond = \
                        PackValueForContext._build_condition(
                            modelcls,
                            self.condition
                        )
                    try:
                        res = modelcls.objects.exclude(
                            **exclude_cond
                        ).filter(
                            **filter_cond
                        )
                        res = res[0].id
                    except:
                        res = None
                    if not res and self.gm:
                        res = GM(modelcls, self.condition).get().id

                    return res

    @staticmethod
    def _build_condition(modelcls, condition):
        """
        Для моедли modelcls строим рекурсивный обход для поиска связей,
        указанных в conditions

        :param modelcls: модель, для которой получаем фильтры
        :type modelcls: django.db.model
        :param condition: условия, по которым строим фильтры
        :type condition: dict
        :return: filter, exclude - фильтры поиска/критерии создания записей БД
        :rtype: tuple of dict
        """
        filter_cond = {}
        exclude_cond = {}
        find_filter_obj = []

        for obj_tp, obj_id in six.iteritems(condition):
            if obj_tp == modelcls:
                if type(obj_id) == int:
                    obj_id = [obj_id]

                filter_cond['pk__in'] = obj_id
                find_filter_obj.append(obj_tp)

        # ищем в текущих полях выбранное ОУ
        for i in get_meta_for_model(modelcls).fields:
            if i.name == 'name' or i.name == 'fullname':
                # в кортежах БД могут быть служебные для теста парметры,
                # например юзеры dev_test
                exclude_cond['%s__icontains' % i.name] = 'dev_test'
            if isinstance(i, models.ForeignKey):
                for obj_tp, obj_id in six.iteritems(condition):
                    if obj_tp not in find_filter_obj:
                        if type(obj_id) == int:
                            obj_id = [obj_id]
                        if i.rel.to is obj_tp:
                            filter_cond[i.name + '__id__in'] = obj_id
                            find_filter_obj.append(obj_tp)

        # не нашли, уходим в рекурсию
        for obj_tp, obj_id in six.iteritems(condition):
            if type(obj_id) == int:
                obj_id = [obj_id]

            if obj_tp not in find_filter_obj:
                name = PackValueForContext._find_recurse_field_in_model(
                    modelcls,
                    obj_tp,
                    []
                )
                if name:
                    filter_cond[name + '__id__in'] = obj_id

            if modelcls == obj_tp:
                filter_cond['id__in'] = obj_id

        return filter_cond, exclude_cond

    @staticmethod
    def _find_recurse_field_in_model(model, m, exclude_model):
        """
        Бегаем по FK и ищем где спрятан unit
        model - где ищем
        m - что ищем
        exclude_model - список моделей, которые уже просмотрены
        """
        name = None
        for i in get_meta_for_model(model).fields:
            if i not in exclude_model and\
                isinstance(i, models.ForeignKey) and\
                    not i.blank:
                exclude_model.append(i)
                if i.rel.to is m:
                    name = i.name
                    break
                name = PackValueForContext._find_recurse_field_in_model(
                    i.rel.to,
                    m,
                    exclude_model
                )
                if name:
                    name = '%s__%s' % (i.name, name)
                    break
        return name


class ModelValueForContext(object):
    """
    Класс для поиска и генерации значений по классу
    """
    def __init__(self, model, condition, gm=False):
        """
        Инициализация созданного объекта

        :param model: модель, для которой получаем или генерируем данные
        :type model: django.db.model
        :param condition: условия, по которым ищем или генерируем данные
        :type condition: dict
        :param gm: gm=True, генерируем, в противном случае - нет
        :type gm: bool
        """
        self.model = model  # модель, для которой ищем/генерируем значения
        self.condition = copy.copy(condition)  # словарь условий, {Model: id}
        # Если не нашли в БД, генерируем или нет, по умолчанию нет
        self.gm = gm

    def get(self):
        """
        Основной метод получения/генерации id объекта модели из БД

        :return: id объекта модели
        :rtype: int
        """
        filter_cond, exclude_cond = PackValueForContext._build_condition(
            self.model,
            self.condition
        )

        modelcls = self.model
        if VirtualModel in modelcls.__mro__ or\
                ModelProxy in modelcls.__mro__:
            modelcls = modelcls.model

        try:
            res = modelcls.objects.exclude(
                **exclude_cond
            ).filter(
                **filter_cond
            )[0].id
        except:
            res = None

        if not res and self.gm:
            res = GM(modelcls, self.condition).get().id

        return res


class GM(object):
    """
    Класс для генерации значений по модели и условию
    """
    def __init__(self, model, condition):
        """
        Инициализация созданного объекта

        :param model: модель, для которой получаем или генерируем данные
        :type model: django.db.model
        :param condition: условия, по которым ищем или генерируем данные
        :type condition: dict
        """
        self.modelcls = model
        if VirtualModel in self.modelcls.__mro__ or\
                ModelProxy in self.modelcls.__mro__:
            self.modelcls = self.modelcls.model
        self.condition = condition

    def get(self):
        """
        Основной метод генерации id объекта модели из БД

        :return: id объекта модели
        :rtype: int
        """
        obj = self.modelcls()

        date_condition = None
        time_condition = None
        datetime_condition = None

        uniq_context = {}
        for i in get_meta_for_model(self.modelcls).fields:

            # наследуемые классы, создается все скопом из текущего
            if i.name.endswith('_ptr'):
                continue

            # это можно не заполнять, но пусть поле name будет всегда
            if i.blank and i.null and i.name != 'name':
                if isinstance(i, models.ForeignKey):
                    if i.rel.to not in self.condition:
                        continue
                else:
                    if i.name not in self.condition:
                        continue

            if hasattr(i, 'choices') and i.choices:
                condition_value = self.condition.get(i.name, None)
                if condition_value:
                    val = condition_value
                else:
                    val = (
                        i.choices[0][0] if i.choices[0][0] else i.choices[1][0]
                    )

                setattr(obj, i.name, val)
            elif isinstance(i, models.ForeignKey):
                from django.contrib.auth.models import User
                exclude_find_model = [User, ]

                res = None
                if i.rel.to not in exclude_find_model:
                    filter_cond, exclude_cond = \
                        PackValueForContext._build_condition(
                            i.rel.to,
                            self.condition
                        )
                    try:
                        res = i.rel.to.objects.exclude(
                            **exclude_cond
                        ).filter(
                            **filter_cond
                        )[0]
                    except IndexError:
                        if i.rel.to in self.condition and\
                                self.condition[i.rel.to]:
                            try:
                                if type(self.condition[i.rel.to]) == int:
                                    obj_id = self.condition[i.rel.to]
                                else:
                                    obj_id = self.condition[i.rel.to][0]
                                res = get_obj_by_id(i.rel.to, obj_id)
                            except (AttributeError, IndexError):
                                pass
                key = '%s_id' % i.name

                uniq_context[key] = None
                if res:
                    uniq_context[key] = res.id
                    # проверяем, что найденное поле соответсвует
                    # всем критериям на уникальность
                    uniq_context = gen_uniq(
                        uniq_context,
                        self.modelcls,
                        self.condition
                    )

                if not uniq_context[key]:
                    uniq_context[key] = GM(i.rel.to, self.condition).get().id

                setattr(obj, key, uniq_context[key])

            elif isinstance(i, models.CharField) or\
                    isinstance(i, models.TextField):
                condition_value = self.condition.get(i.name, None)
                if condition_value:
                    val = condition_value
                elif i.name in ['last_name', 'first_name', 'middle_name']:
                    ml = getattr(i, 'max_length', 55)
                    val = GM.str_generator(ml if ml < 55 else 55)
                elif i.name.startswith('time') or i.name.endswith('time'):
                    val = '%s:%s' % (
                        random.randint(0, 23),
                        random.randint(0, 59)
                    )
                else:
                    val = GM.str_generator(
                        getattr(i, 'max_length', 255) or 255
                    )
                setattr(obj, i.name, val)

            elif isinstance(i, models.TimeField):
                val = datetime.datetime.now()
                delta_hour = datetime.timedelta(seconds=60 * 60)
                condition_value = self.condition.get(i.name, None)
                if condition_value:
                    val = condition_value
                elif 'begin' in i.name or 'start' in i.name:
                    if time_condition is not None:
                        val = time_condition - delta_hour
                    else:
                        time_condition = val
                if 'end' in i.name or 'finish' in i.name:
                    if time_condition is not None:
                        val = time_condition + delta_hour
                    else:
                        time_condition = val

                if hasattr(self.modelcls, '_extract_time'):
                    val = val.time().strftime('%H:%M')
                else:
                    val = val.time()

                setattr(obj, i.name, val)

            elif isinstance(i, models.DateField):
                val = datetime.datetime.now()
                condition_value = self.condition.get(i.name, None)
                if condition_value:
                    val = condition_value
                elif 'begin' in i.name or 'start' in i.name:
                    if date_condition is not None:
                        val = date_condition - datetime.timedelta(days=5)
                    else:
                        date_condition = val
                if 'end' in i.name or 'finish' in i.name:
                    if date_condition is not None:
                        val = date_condition + datetime.timedelta(days=5)
                    else:
                        date_condition = val

                val = val.date()

                setattr(obj, i.name, val)

            elif isinstance(i, models.DateTimeField):
                val = datetime.datetime.now()
                day_delta = datetime.timedelta(days=5, seconds=60 * 60)
                condition_value = self.condition.get(i.name, None)
                if condition_value:
                    val = condition_value
                elif 'begin' in i.name or 'start' in i.name:
                    if datetime_condition is not None:
                        val = datetime_condition - day_delta
                    else:
                        datetime_condition = val
                if 'end' in i.name or 'finish' in i.name:
                    if datetime_condition is not None:
                        val = datetime_condition + day_delta
                    else:
                        datetime_condition = val
                setattr(obj, i.name, val)

            elif isinstance(i, models.BooleanField):
                condition_value = self.condition.get(i.name, None)
                if condition_value:
                    val = condition_value
                else:
                    val = random.randint(0, 1)
                setattr(obj, i.name, val)

            # SmallIntegerField instance IntegerField
            elif isinstance(i, models.SmallIntegerField):
                condition_value = self.condition.get(i.name, None)
                if condition_value:
                    val = condition_value
                else:
                    val = random.randint(0, 32767)
                setattr(obj, i.name, val)

            elif isinstance(i, (models.IntegerField, models.DecimalField,
                            models.FloatField)):
                condition_value = self.condition.get(i.name, None)
                if condition_value:
                    val = condition_value
                else:
                    max_length = getattr(i, 'max_length', 4) or 4
                    if max_length > 9:
                        max_length = 9
                    val = random.randint(0, 10**max_length)
                setattr(obj, i.name, val)

            elif isinstance(i, models.FileField):
                basedir = os.path.join(
                    settings.MEDIA_ROOT,
                    'test_files',
                )
                if not os.path.exists(basedir):
                    os.makedirs(basedir)

                path = os.path.join(
                    basedir,
                    GM.str_generator(
                        (getattr(i, 'max_length', 255) or 255) -
                        len(basedir) - 1
                    )
                )

                created_file = open(path, "w+")
                # wipe the existing content
                created_file.truncate()

                created_file.close()
                setattr(obj, i.name, path)

        obj_not_valid = True
        while obj_not_valid:
            try:
                obj.validate_unique()
                obj_not_valid = False
            except ValidationError:
                uniq_list = list(
                    get_meta_for_model(
                        self.modelcls
                    ).unique_together
                )
                for uniq_tuple in uniq_list:
                    if not any([i.endswith('id') for i in uniq_tuple]):
                        for uniq in uniq_tuple:
                            param = getattr(obj, uniq)
                            if param:
                                if isinstance(param, datetime.date):
                                    param += datetime.timedelta(
                                        days=5,
                                        seconds=60 * 60
                                    )
                                elif isinstance(param, six.string_types):
                                    param = GM.str_generator(len(param))
                                else:
                                    param += 1
                                setattr(obj, uniq, param)
            # raise BitField
            except TypeError:
                obj_not_valid = False
            except AttributeError:
                obj_not_valid = False
        try:
            obj.save()
        except Exception as ex:
            ex.args = (ex.args if ex.args else tuple()) + (self.modelcls,)
            raise

        return obj

    @staticmethod
    def str_generator(size=6, chars=string.ascii_lowercase):
        """
        Возвращает произвольную строку длины size

        :param size: условия, размер будущей строки
        :type size: int
        :param chars: символы, которые будут учавствовать в генерации
        :type chars: str
        :return: сгенерированная произвольная строка
        :rtype: str
        """
        return ''.join(random.choice(chars) for x in range(size))


class GMWindowField(object):
    """
    Класс для поиска и генерации значений
    (либо берем из БД, либо создаем свой)
    по записям declare_context
    """
    def __init__(self, pack, win, context, condition):
        """
        Инициализация созданного объекта

        :param objectpack.ObjectpPack pack: инстанс пака
        :param objectpack.BaseEditWindow win: инстанс окна
        :param objectpack.dict context: контекст запроса (из setUp)
        :param objectpack.dict condition: условия генерациия для моделей
        """
        self.pack = pack
        self.win = win
        self.context = context
        self.condition = condition

    @staticmethod
    def get_default_data(some_field, model):
        if isinstance(some_field, ExtStringField):
            temp_field = None
            mask_re = some_field.mask_re
            try:
                temp_field = get_meta_for_model(
                    model
                ).get_field_by_name(some_field.name)
            except:
                pass

            if temp_field is not None:
                if isinstance(temp_field[0], models.TimeField):
                    return u'12:12'

            if hasattr(some_field, 'regex') and some_field.regex and\
                    re.match(some_field.regex, u'12:12'):
                return u'12:12'

            gen_param = {}
            if mask_re:
                all_chars = u''.join([
                    u'абвгдеёжзийклмнопрстуфхцчшщьъэюяa',
                    string.ascii_lowercase,
                    '0123456789'])
                nchars = re.findall(mask_re, all_chars)
                gen_param.update({'chars': nchars})
            if hasattr(some_field, 'max_length') and some_field.max_length:
                gen_param.update({'size': some_field.max_length})
            return GM.str_generator(**gen_param)

        elif isinstance(some_field, (ExtHTMLEditor, ExtTextArea)):
            return GM.str_generator()
        elif isinstance(some_field, ExtNumberField):
            return 111
        elif isinstance(some_field, ExtDateTimeField):
            return format(datetime.datetime.now(), '%d.%m.%Y %H:%M:%S')
        elif isinstance(some_field, ExtDateField):
            return format(datetime.datetime.today(), '%d.%m.%Y')
        elif isinstance(some_field, ExtCheckBox):
            return False
        elif isinstance(some_field, ExtFileUploadField):
            basedir = os.path.join(
                settings.MEDIA_ROOT,
                'test_files',
            )
            if not os.path.exists(basedir):
                os.makedirs(basedir)

            file_name = '%s.jpeg' % (
                GM.str_generator(50),
            )

            file_path = os.path.join(
                basedir,
                file_name,
            )
            if isinstance(some_field, ExtImageUploadField):
                import Image
                pystr = ""
                for i in range(30*30*4):
                    pystr += str(i)
                im_out = Image.fromstring("RGBA", (30, 30), pystr)
                im_out.save(file_path, format='jpeg')
            else:
                created_file = open(file_path, "w+")
                # wipe the existing content
                created_file.truncate()

                created_file.close()
            return {
                'file_%s' % some_field.name: (open(file_path, 'rb')),
                some_field.name: file_name
            }
        return None

    def get(self):

        all_fields = []
        temp_tabs = None

        instance_aw = self.win
        context_new = self.context

        if isinstance(instance_aw, TabbedEditWindow):
            temp_tabs = instance_aw.tabs
        elif isinstance(instance_aw, BaseEditWindow):
            temp_tabs = []
            for i in dir(instance_aw):
                if isinstance(getattr(instance_aw, i), WindowTab):
                    temp_tabs.append(getattr(instance_aw, i))
        if temp_tabs:
            for tab in temp_tabs:
                temp_some_fields = list(tab.__dict__.values())
                for some_cur_field in temp_some_fields:
                    if isinstance(some_cur_field, list):
                        all_fields.extend(some_cur_field)
                    else:
                        all_fields.append(some_cur_field)
        all_fields.extend(list(instance_aw.__dict__.values()))

        # Табы. Если есть, берем все поля и генерим по ним данные
        for ex_local_filed in all_fields:
            if isinstance(ex_local_filed, BaseExtField):
                if ex_local_filed.name not in context_new:
                    store = getattr(ex_local_filed, 'store', None)
                    if ex_local_filed.name and ex_local_filed.name not in context_new:
                        if store:
                            if getattr(store, 'data', None):
                                try:
                                    context_new[ex_local_filed.name] =\
                                        store.data[0][0]
                                except IndexError:
                                    pass
                            else:
                                y_model = getattr(
                                    ex_local_filed.pack,
                                    'model',
                                    None
                                ) or\
                                    getattr(
                                        ex_local_filed.pack,
                                        'tree_model',
                                        None
                                    )
                                if y_model:
                                    context_new[ex_local_filed.name] =\
                                        ModelValueForContext(
                                            model=y_model,
                                            condition=self.condition,
                                            gm=True
                                        ).get()
                        else:
                            for_new_context = GMWindowField.get_default_data(
                                ex_local_filed, self.pack.model)
                            if for_new_context:
                                if isinstance(for_new_context, dict):
                                    context_new.update(for_new_context)
                                else:
                                    if ex_local_filed.name not in context_new:
                                        context_new[ex_local_filed.name] =\
                                            for_new_context
            else:
                try:
                    from kladr.addrfield import ExtAddrComponent
                    if isinstance(ex_local_filed, ExtAddrComponent):
                        for i in [
                                'place', 'street',
                                'house', 'zipcode',
                                'addr', 'corps',
                                'flat'
                        ]:
                            if not getattr(
                                    ex_local_filed,
                                    '%s_allow_blank' % i,
                                    True
                            ) or i in ['zipcode', 'addr']:
                                key = getattr(
                                    ex_local_filed,
                                    '%s_field_name' % i,
                                    None
                                )
                                if key not in context_new:
                                    context_new[key] = \
                                        random.randint(0, 10**5)
                except ImportError:
                    pass

        return context_new
