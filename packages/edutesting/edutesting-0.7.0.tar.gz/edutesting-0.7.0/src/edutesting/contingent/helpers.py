# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

from random import randint
from random import sample
import six
from six.moves import range


SNILS_LIST = []


def get_key_by_value(source, value):
    u"""
    :param source: Словарь или список choices модели для поиска
    :param value: Искомое значение
    :return: Ключ соответствующий значению
    """
    if isinstance(source, list) or isinstance(source, tuple):
        source = dict(item for item in source)
    for k, v in six.iteritems(source):
        if not isinstance(v, six.string_types):
            item = v.value
        else:
            item = v
        if value == item:
            return k

    raise KeyError('Value "{}" does not exist'.format(value))


def get_snils():
    u"""
    :return: СНИЛС в формате xxx-xxx-xxx xx
    """
    def get_check_sum(current_sum):
        check = current_sum
        while check > 100:
            check %= 101
        else:
            if check == 100:
                check = 0
        return check

    while True:
        numbers = sample(range(10), 9)
        if numbers not in SNILS_LIST:
            SNILS_LIST.append(numbers)
            break

    str_num = [str(n) for n in numbers]
    multipls = list(range(1, 10))
    multipls.reverse()
    numbers = [numbers[i] * multipls[i] for i in range(len(numbers))]
    num_sum = sum(numbers)
    check_sum = '%02d' % (get_check_sum(num_sum))

    for i in (3, 7):
        str_num.insert(i, '-')

    return ' '.join([''.join(str_num), check_sum])


def replace_spec_symbols(value, symbols_list):
    u"""
    :param value: Строка в которой нужно убрать спец. символы.
    :param symbols_list: Список сиволов для замены.
    :return: Строка, где символы заменены на ''.
    """
    s = value
    for symbol in symbols_list:
        s = s.replace(symbol, '')
    return s


def get_random_value(catalog):
    u"""
    :param catalog: Список 'choices'
    :return: Индекс записи
    """
    count = len(catalog)
    return catalog[randint(0, count-1)][0]
