# -*- coding: utf-8 -*-
"""
базовые классы тестирования
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import unittest
import re
import os
import sys

from django.conf import settings


class BaseTest(unittest.TestCase):
    """
    Базовый класс для всех видов тестрования
    Можно сделать наследование от django.test.simple.TestCase,
        тогда БД мокается
    """
    ru_speller = None

    def __init__(self, *args, **kwargs):
        """
        Инициализация созданного объекта
        """
        self.enc = ''
        try:
            import aspell

            speller_args = [
                ('lang', 'ru'),
                ('encoding', 'utf-8'),
            ]

            path = os.path.join(settings.PROJECT_ROOT, '.aspell.ru.pws')
            if os.path.isfile(path):
                speller_args.append(('personal-path', path))

            path = os.path.join(settings.PROJECT_ROOT, '.aspell.ru.prepl')
            if os.path.isfile(path):
                speller_args.append(('repl-path', path))

            self.ru_speller = aspell.Speller(*speller_args)

        except ImportError:
            sys.stdout.write('Import error Aspell. Test without check test\n')
            self.ru_speller = None
        super(BaseTest, self).__init__(*args, **kwargs)

    def check_spell(self, words):
        '''
        Проверка офрографии

        Установка apt-get install aspell libaspell-dev aspell-en aspell-ru

        python-aspell
        http://0x80.pl/proj/aspell-python/index-c.html

        пример вызова для рус.языка. словарь может быть в любой кодировке
        self.ru_speller.check(u'привет'.encode(enc))

        с англ.все проще
        self.en_speller.check('hello')
        '''

        d2r_table = [
            'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX',
            'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC',
            'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM']

        spell_frase = True
        words = words.replace(u'Кол-ва', '').replace(u'кол-ва', '')
        splitters = r'[\s/\\,\.()-0123456789\'\!?:"]+'
        if self.ru_speller is not None:
            for word in re.split(splitters, words, re.U):
                if word != '' and word not in d2r_table:
                    spell_frase = spell_frase and\
                        self.ru_speller.check(word.encode('utf-8'))
        return spell_frase
