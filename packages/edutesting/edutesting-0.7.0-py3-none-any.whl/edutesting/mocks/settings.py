# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import os

settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')
if not settings_module:
    raise AttributeError('Set DJANGO_SETTINGS_MODULE variable')

PROJECT = settings_module.split('.')[0]
if PROJECT == 'web_edu':
    from web_edu.livesettings import config as settings
else:
    from django.conf import settings
RECIPIENT_MNEMONIC = getattr(settings, 'SMEV_SYS_MNEMONICS')

CONFIG_PATH = '_'.join([PROJECT.upper(), 'CONFIG_PATH'])
CURRENT_CONFIG_PATH = os.environ.get(CONFIG_PATH)
if CURRENT_CONFIG_PATH:
    CERT_PATH = os.path.join(CURRENT_CONFIG_PATH, 'lipetsk_smev.pem')
    DT_EXCHANGE_LOG_FILE = os.path.join(CURRENT_CONFIG_PATH, 'dt_log')
else:
    raise AttributeError('Set "{}" variable'.format(CONFIG_PATH))


MODE_ALL = 'ALL'
MODE_UPDATE = 'UPDATE'
