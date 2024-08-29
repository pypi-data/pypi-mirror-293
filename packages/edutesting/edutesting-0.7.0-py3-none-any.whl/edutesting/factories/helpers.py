# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

from edutesting.contingent.helpers import get_key_by_value

from datetime import datetime
import six


def check_str(func):
    u"""
    Декоратор для проверки параметра на принадлженость строковому типу.
    Если параметр является строкой, то передаем его на обработку функции,
    если нет, то возвращаем исходный резултат.
    Применяется для проверки данных в фабриках тестовых данных.
    """
    def wrapper(*args, **kwargs):
        if isinstance(kwargs['value'], six.string_types):
            result = func(*args, **kwargs)
        else:
            result = kwargs['value']
        return result
    return wrapper


@check_str
def str_to_model_instance(model, request, value):
    u"""
    Ф-ия для получения соответствующего инстанса модели.
    Применяется для проверки данных в фабриках тестовых данных.
    :param model: Класс Django-модели
    :param request: Словарь для формирования запроса
    :param value: Исходное строковое значение
    """
    return model.objects.get(**request)


@check_str
def str_to_choices_idx(choices, value):
    u"""
    Ф-ия для получения соответствующего индеса из choices.
    Применяется для проверки данных в фабриках тестовых данных.
    :param choices: Список choices
    :param value: Исходное строковое значение
    """
    return get_key_by_value(choices, value)


@check_str
def str_to_bool(value):
    u"""
    Ф-ия для преобразования в булевое значение исходной строки.
    Применяется для проверки данных в фабриках тестовых данных.
    :param value: Исходная строка
    """
    return value.lower() == 'да'


@check_str
def str_to_date(value, date_format='%d.%m.%Y'):
    u"""
    Ф-ия для преобразования исходной строки в дату по указанному формату.
    Применяется для проверки данных в фабриках тестовых данных.
    :param value: Исходная строка.
    :param date_format: Формат.
    """
    return datetime.strptime(value, date_format)


@check_str
def str_to_num(value, num_type=int):
    u"""
    Ф-ия для преобразования исходной строки в указанный числовой тип.
    Применяется для проверки данных в фабриках тестовых данных.
    :param value: Исходная строка.
    :param num_type: Числовой класс.
    """
    return num_type(value)
