# -*- coding: utf-8 -*-
u"""
Набор степов работы с рабочим столом.
"""
from __future__ import absolute_import
from __future__ import unicode_literals

from behave import step

from .winobject import Desktop


@step(u'Можно нажать кнопку "Пуск"')
def step_can_click_start_button(context):
    u"""
    :param context: behave-контекст степа.
    """
    desktop = Desktop(context.browser)
    assert desktop.can_click_start_button(context), (
        u'Кнопка "Пуск" не найдена'
    )


@step(u'Пуск -> {elements}')
def step_menu_start(context, elements):
    u"""
    Выбор элемента в меню Пуск

    :param context: behave-контекст степа.
    :param elements: строка с указанием пути до нужного элемента меню,
      элементы пути разделены знаком ->
      (прим. Поурочное планирование -> Учебные планы -> Базисные учебные планы)
    """
    dp = Desktop(context.browser)
    dp.select_start_menu_item(elements, context)


@step(u'в виджетах нажать выбрать организацию')
def step_select_unit(context):
    u"""
    Вызов окна Учреждения путем нажатия кнопки Выбрать в виджете Учреждение.
    """
    dp = Desktop(context.browser)
    dp.select_school()


@step(u'в виджетах нажать сбросить организацию')
def step_reset_unit(context):
    u"""
    Сбрасывает выбранное учреждение путем нажатия
    кнопки Сбросить в виджете Учреждение.
    """
    dp = Desktop(context.browser)
    dp.reset_school()


@step(u'в виджетах нажать выбрать период')
def step_select_period(context):
    u"""
    Вызов окна Периоды обучения путем нажатия кнопки Выбрать в
    виджете Период обучения.
    """
    dp = Desktop(context.browser)
    dp.select_period()


@step(u'на рабочем столе есть иконка "{icon_name}"')
def step_find_icon_on_desktop(context, icon_name):
    u"""
    Проверка что на рабочем столе есть иконка с названием icon_name

    :param context: behave-контекст степа.
    :param icon_name: Название иконки.
    """
    dp = Desktop(context.browser)
    assert dp.is_icon_exists(icon_name)


@step(u'на рабочем столе кликнуть на иконку "{icon_name}"')
def step_click_desktop_item(context, icon_name):
    u"""
    Производит клик по иконке icon_name с целью вызова окна.

    :param context: behave-контекст степа.
    :param icon_name: Название иконки.
    """
    dp = Desktop(context.browser)
    dp.click_by_icon(icon_name)
