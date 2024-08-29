# coding: utf-8
from __future__ import unicode_literals

from __future__ import absolute_import
from functools import wraps
from xvfbwrapper import Xvfb


def xvfb(width=800, height=600, color=24, **kwargs):
    u"""
    Декоратор для работы с виртуальным дисплеем.
    Если при запуске behave был указан параметр
    -D VISIBLE=False, то дисплей будет запущен при
    выполнении before_all хука, и завершен при
    выполнении after_all хука.

    :param width: Ширина
    :type width: int
    :param height: Высота
    :type height: int
    :param color: Глубина цвета
    :type color: int
    :param kwargs: Дополнительные параметры
    """

    def decorator(func):
        @wraps(func)
        def wrapper(context):
            is_visible = context.config.userdata.getbool('VISIBLE', True)
            func_name = func.__name__
            if not is_visible:
                if func_name == 'before_all':
                    context.vdisplay = Xvfb(
                        width=width,
                        height=height,
                        colordepth=color,
                        **kwargs
                    )
                    context.vdisplay.start()
                elif func_name == 'after_all':
                    context.vdisplay.stop()

            func(context)
        return wrapper
    return decorator
