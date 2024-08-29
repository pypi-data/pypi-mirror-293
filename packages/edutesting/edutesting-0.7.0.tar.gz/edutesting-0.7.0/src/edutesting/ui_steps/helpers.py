# -*- coding: utf-8 -*-
u"""
Набор вспомогательных фун. для селениум тестов.
"""
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import time

from functools import wraps

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


TEXT = 1
NUMBER = 2
BLANK = 6

WAIT_AJAX_BEGIN = 0.4
GENERIC_WAIT = 5

MONTHS = {
    u'Январь': 1,
    u'Февраль': 2,
    u'Март': 3,
    u'Апрель': 4,
    u'Май': 5,
    u'Июнь': 6,
    u'Июль': 7,
    u'Август': 8,
    u'Сентябрь': 9,
    u'Октябрь': 10,
    u'Ноябрь': 11,
    u'Декабрь': 12,
}

"""
Индексы для полей, расположенных в блоках fieldset
с соответствующими именами
"""
FIELDSET_NAMES = {
    u'Фактический адрес': '',
    u'Адрес регистрации по месту жительства': '-1',
    u'Адрес регистрации по месту пребывания': '-2',
    u'Адрес регистрации по месту пребывания ученика': '-2'
}

# Кортеж с подгружаемыми js-файлами.
# Необходим для того, чтобы зафиксировать порядок подгрузки.
HELPER_FILES = (
    'esprima.js',
    'SJTXE.js',
    'helpers.js',
    'journal.js',
    'ui.js',
    'winobject.js',
)


def inject_js_script(driver, file_path):
    f = open(file_path, 'r')
    driver.execute_script(f.read())


def execute_required_js(driver):
    path = os.path.join(os.path.dirname(__file__), 'js_scripts')
    for file_name in HELPER_FILES:
        inject_js_script(driver, path + '/' + file_name)


def load_js(function):
    """
    Декоратор для загрузки js кода. Навешивается на функцию before_step в
    файле enviroment.py. И перед каждым степом проверяет
    загружены ли необходимые js библиотеки.
    """
    @wraps(function)
    def wrapper_load_js(arg_context, arg_step):
        if hasattr(arg_context, 'browser'):
            js_helpers_not_load = arg_context.browser.execute_script(
                """return (typeof ui === 'undefined')""")
            if (js_helpers_not_load and
                arg_context.TEST_URL in arg_context.browser.current_url and
                    not arg_context.personal_area_interface):
                execute_required_js(arg_context.browser)
            elif arg_context.personal_area_interface:
                intercept_jquery_ajax(arg_context.browser)
            function(arg_context, arg_step)
    return wrapper_load_js


def is_ext_defined(driver):
    """
    Проверяем доступен ли объект Ext на текущей странице. Необходим т.к.
    например в интерфейсе ученика/родителя ExtJS не используется.
    """
    time.sleep(WAIT_AJAX_BEGIN)
    return driver.execute_script("""
        return !(typeof(Ext) == 'undefined');
    """)


def waitForExtAjax(context):
    """
    Ждем пока завершатся все Ajaxы у Ext
    """
    context.webdriverwait.until(lambda driver: driver.execute_script("""
        return typeof Ext != 'undefined' && !Ext.Ajax.isLoading()
        || (typeof SJTXE !== "undefined" && SJTXE.hasAjaxFailure());
    """))


def waitForJQueryAjax(context):
    """
    Ждем пока завершатся все Ajaxы у JQuery
    """
    context.webdriverwait.until(lambda driver: driver.execute_script("""
            return typeof jQuery != 'undefined' && jQuery.active == 0;
        """))


def intercept_jquery_ajax(driver):
    """
    Перехватываем все Ajax-ответы jQuery. Применяется для получения
    имени скачиваемых файлов.
    """
    driver.execute_script("""
        $(document).ajaxComplete(function(event, xhr, settings) {
            if (xhr.responseText.indexOf('media/downloads') != -1) {
                file_name = xhr.responseText.slice(
                    xhr.responseText.indexOf("/media"),
                    xhr.responseText.indexOf("xls")+3
                );
                window.reportFileName = file_name.split('/').pop();
            } else {
                window.jQueryAjaxResponse = xhr.responseText;
            }
        });
    """)


def waitForImport(context):
    """
    Ждем завершение импорта файла
    """
    context.webdriverwait.until(lambda driver: driver.execute_script("""
        return window.responseImport;
    """))


def get_toolbar_id_by_column_name(context, win_id, column_name):
    window = context.browser.find_element_by_id(win_id)
    toolbars = window.find_elements_by_class_name('x-grid-panel')
    for toolbar in toolbars:
        columns = toolbar.find_elements_by_class_name('x-grid3-hd-inner')
        for column in columns:
            if column.text == column_name:
                return toolbar.get_attribute('id')
    return 0


def get_modal_win_id_by_name(context, win_name):
    win_name = u' ' if win_name == u'None' else win_name
    windows = context.webdriverwait.until(
        lambda driver: driver.find_elements_by_xpath(
            "//div[(contains(@class, 'x-window') "
            "or contains(@class, ' x-window'))"
            " and contains(@id, 'ext-comp')]")
    )
    for window in windows:
        header = window.find_element_by_class_name('x-window-header-text')
        if header.text == win_name:
            return window.get_attribute('id')
    return 0


def select_journal_cell(context, grid_id, date, time, header, pupil_name):
    context.browser.execute_script("""
        helpers.find_and_select_row('{0}', '{1}', '{2}', '{3}', '{4}')
        """.format(grid_id, date, time, header, pupil_name)
    )


def path_to_resource_file(file_name, resource_dir):
    """
    :param resource_dir: Путь к директории в которой храниться файл.
    """
    path_to_file = (resource_dir + '/' + file_name)
    assert os.path.exists(path_to_file)
    return path_to_file


def is_tab_with_title_open(context, win_title):
    """
    В большинстве тестов все действия происходят одном окне поэтому
    при проверке открылась ли новая вкладка можно
    проверить вкладку с индексом 1.
    """
    context.browser.switch_to.window(context.browser.window_handles[1])
    cur_title = context.browser.title
    context.browser.switch_to.window(context.browser.window_handles[0])
    return win_title in cur_title


def get_report_file_name(context):
    file_name = context.browser.execute_script(u"""
        return window.reportFileName;
    """) or ''
    try:
        file_name = file_name.decode('unicode_escape')
    except UnicodeEncodeError:
        pass
    return file_name


def is_elem_exists(driver, elem_id):
    return len(driver.find_elements_by_id(elem_id)) > 0


def editor_input_value(driver, editor_id):
    return driver.execute_script(u"""
        return Ext.getCmp('{0}').getRawValue();
    """.format(editor_id))


def convert_cell_value(cell):
    """
    Приводит значение ячейки Excel документа к типу str.
    :param cell:
    :return: String cell value
    :rtype: str
    """
    if cell.ctype == TEXT:
        return cell.value
    elif cell.ctype == NUMBER:
        if cell.value == int(cell.value):
            return '{0:d}'.format(int(cell.value))
        else:
            return '{0:.2f}'.format(cell.value)
    elif cell.ctype == BLANK:
        return ''
