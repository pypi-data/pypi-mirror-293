# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals

import time
import os

from functools import wraps
from hashlib import md5


IMAGE = 'png'
HTML = 'html'


def sec2ms(sec):
    return int(round(sec * 1000.0))


def now_in_ms():
    u"""
    Возвращает текущее время в формате совместимом с отчетами allure
    """
    return str(sec2ms(time.time()))


def replace_dots(string):
    return string.replace('.', '')


def set_current_time(func):
    u"""
    Декоратор для behave хуков из environment файла. Добавляет аттрибут
    содержащий время начала или конца выполнения behave_model.
    Behave_model может быть Feature, Scenario, Step.
    """
    @wraps(func)
    def wrapper(context, behave_model):
        f_name = func.__name__
        attr_name = 'start'
        if u'after' in f_name:
            attr_name = 'stop'

        setattr(behave_model, attr_name, now_in_ms())
        func(context, behave_model)
    return wrapper


def create_attachment(png_sting, path_to_save, attachment_type=IMAGE):
    u"""
    Сохраняет скриншот с именем в формате {HASH-SUM}-attachment.png.
    :param png_sting: Строка с содержимым файла
    :param path_to_save: Путь куда будет сохранен файл
    :param attachment_type: Тип файла. По умполчания image.
    :return: Имя файла
    """
    hash_sum = md5(png_sting).hexdigest()
    filename = '-'.join((hash_sum, 'attachment.' + attachment_type,))
    file_path = os.path.join(path_to_save, filename)

    with open(file_path, 'wb') as f:
        f.write(png_sting)
    return filename
