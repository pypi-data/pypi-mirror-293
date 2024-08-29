# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import six.moves.urllib.parse

from behave import step, given

from .helpers import waitForJQueryAjax


def remove_clock(context):
    context.browser.execute_script(
        """
        (function(){
            'use strict';
            $('#clock').remove();
        })()
        """
    )


@step(u'страница приветствия')
def login_hello_page(context):
    context.browser.get(context.TEST_URL)
    main = context.browser.page_source
    assert 'login_login' in main and 'login_password' in main


@step(u'откроется страница рабочего стола')
def login_desk_page(context):
    u"""
    Ожидает открытия рабочего стола.
    """
    context.browser.get(six.moves.urllib.parse.urljoin(context.TEST_URL, 'desk'))
    remove_clock(context)


@step(u'Авторизоваться в системе, нажав кнопку Войти на старнице приветсвия')
def step_click_enter_in_main_page(context):
    u"""
    Нажатие кнопки отправить для авторизации в системе.
    """
    elem = context.browser.find_element_by_xpath("//input[@type='submit']")
    elem.click()
    waitForJQueryAjax(context)
    remove_clock(context)


@given(
    u'супер-администратор c логином {login_login} и паролем {login_password}'
)
def given_login_hello_page(context, login_login, login_password):
    u"""
    Осуществляет авторизацию пользователя в с логином login_login и паролем
    login_password в системе.
    """
    # TODO: данный подход неприемлем потому что
    #      это смешение уровней абстракции.
    #      Чтобы лучше понимать, что происходит,
    #      python и behave нужно разделять.
    context.execute_steps(u'Дано страница приветствия')
    context.execute_steps(
        u'Если Ввести в поле login_login значение %s' % login_login)
    context.execute_steps(
        u'Если Ввести в поле login_password значение %s' % login_password)
    context.execute_steps(
        u'Если Авторизоваться в системе, '
        u'нажав кнопку Войти на старнице приветсвия'
    )


@given(u'выбрано в виджете текущее ОУ {OU}')
def given_unit(context, OU):
    # TODO: данный подход неприемлем потому что
    #      это смешение уровней абстракции.
    #      Чтобы лучше понимать, что происходит,
    #      python и behave нужно разделять.
    context.execute_steps(u'Если в виджетах нажать выбрать организацию')
    context.execute_steps(
        u'Если в древоводином окне Организации выбрать запись %s '
        u'по колонке Наименование' % OU)
    context.execute_steps(
        u'Если в окне Организации в нижней панели нажать кнопку Выбрать')
    context.execute_steps(u'То откроется страница рабочего стола')


@given(u'выбран в виджете период обучения {period_name}')
def given_period(context, period_name):
    # TODO: данный подход неприемлем потому что
    #      это смешение уровней абстракции.
    #      Чтобы лучше понимать, что происходит,
    #      python и behave нужно разделять.
    context.execute_steps(u'Если в виджетах нажать выбрать период')
    context.execute_steps(
        u'Если в окне Периоды обучения выбрать запись %s '
        u'по колонке Наименование' % period_name)
    context.execute_steps(
        u'Если в окне Периоды обучения в нижней панели нажать кнопку Выбрать')
    context.execute_steps(u'То закроется окно Периоды обучения')
