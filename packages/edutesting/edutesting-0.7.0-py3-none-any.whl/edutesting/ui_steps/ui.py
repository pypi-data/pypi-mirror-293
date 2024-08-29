# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
import os
from warnings import warn

import xlrd
from behave import step
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from .helpers import convert_cell_value
from .helpers import get_modal_win_id_by_name
from .helpers import get_report_file_name
from .helpers import get_toolbar_id_by_column_name
from .helpers import is_tab_with_title_open
from .helpers import waitForExtAjax
from .helpers import waitForImport
from .winobject import find_win_obj
from .winobject import get_win_object
from .winobject import WinNotFound
import six
from six.moves import range


_DEPRECATION_STEP_STRING = u'Степ устаревший не рекомендуется к использованию'


def _find_and_select_node(context, win_obj, elements, column_name):
    eval_el = find_win_obj(context, win_obj)
    parse_elements = [x.strip() for x in elements.split('->')]

    js_line = u'ui.find_and_select_node(\'{0}\', [\'{1}\'], \'{2}\');'.format(
        eval_el[win_obj]['id'],
        "', '".join(parse_elements),
        column_name
    )
    context.browser.execute_script(js_line)


@step(u'Ввести в поле {element} значение {value}')
def step_fill_element_with_text(context, element, value):
    u"""
    Устанавливает значение value в input c атрибутом name равным element.
    """
    control = "//input[@name='%s']" % element
    elem = context.browser.find_element_by_xpath(control)
    elem.send_keys(value)


@step(u'ввести в текстовое поле {area_name} текст {text}')
def step_fill_textarea_with_text(context, area_name, text):
    xpath = "//textarea[@name='%s']" % area_name
    element = context.browser.find_element_by_xpath(xpath)
    element.send_keys(text)


@step(u'Нажать кнопку {element}')
def step_click_xpath(context, element):
    u"""
    Ищем кнопку по name
    """
    control = "//button[@name='%s']" % element
    elem = context.browser.find_element_by_xpath(control)
    elem.click()


@step(u'откроется окно {win_obj}')
def step_find_win_obj(context, win_obj):
    u"""
    Проверка что открылось окно с именем win_obj:
    Если окно без названия, то в качестве названия
    нужно указать None

    :param context: behave-контекст степа.
    :param win_obj: Название окна.
    """
    win = get_win_object(context, win_obj)
    if not win:
        raise WinNotFound(
            u'Окно с названием "{}" не найдено!'.format(win_obj)
        )


@step(u'закрыть окно {win_obj}')
def step_close_win(context, win_obj):
    u"""
    Закрывает окно с именем win_obj.

    :param context: behave-контекст степа.
    :param win_obj: Название окна.
    """
    win = get_win_object(context, win_obj)
    win.close()


@step(u'окно "{win_obj}" не откроется')
def ste_win_not_open(context, win_obj):
    u"""
    Проверка того что окно с названием win_obj не открылось.
    """
    eval_el = find_win_obj(context, win_obj)
    assert win_obj not in eval_el


@step(u'откроется диалоговое окно {win_obj}')
def step_find_dlg_win(context, win_obj):
    u"""
    Проверка того что открылось оконо c названием win_obj.
    """
    win_id = get_modal_win_id_by_name(context, win_obj)
    if not win_id:
        raise WinNotFound(
            u'Окно с названием "{}" не найдено!'.format(win_obj)
        )


@step(u'закроется окно {win_obj}')
def step_check_close_win_obj(context, win_obj):
    u"""
    Проверка что окно с названием win_obj закрылось.

    Если окно без названия, то в качестве названия нужно указать None
    """
    win = get_win_object(context, win_obj)
    assert not win or win.is_close(), 'Window is open!'


@step(
    u'в окне {win_obj} на вкладке {tab} на '
    u'панели инструментов нажать кнопку {button}'
)
def step_find_win_obj_and_click_button_into_top_toolbar_on_tabs(
        context, win_obj, tab, button
):
    u"""
    Нажать кнопку button на панели грида который находиться на вкладке tab
    окна win_obj.
    """
    eval_el = find_win_obj(context, win_obj)
    button_id = context.browser.execute_script(u"""
    return ui.find_button_into_toolbar('{0}', '{1}', '{2}')
    """.format(eval_el[win_obj]['id'], tab, button))

    elem = context.browser.find_element_by_id(button_id)
    elem.click()


@step(u'в окне {win_obj} на панели инструментов нажать кнопку {button}')
def step_find_win_obj_and_click_button_into_top_toolbar(
    context, win_obj, button
):
    u"""
    Нажать кнопку button на панели инструментов окна.
    """
    eval_el = find_win_obj(context, win_obj)
    window = context.browser.find_element_by_id(eval_el[win_obj]['id'])
    try:
        grid_obj = window.find_element_by_class_name('x-grid-panel')
        grid_obj = grid_obj.get_attribute('id')
    except NoSuchElementException:
        grid_obj = ''

    button_id = context.browser.execute_script(u"""
    return ui.find_button_into_grid_obj('{0}', '{1}', '{2}')
    """.format(eval_el[win_obj]['id'], grid_obj, button))
    elem = context.browser.find_element_by_id(button_id)
    elem.click()


@step(u'в окне {win_obj} в нижней панели нажать кнопку {button}')
def step_find_win_obj_and_click_button_into_toolbar(context, win_obj, button):
    u"""
    Нажатие кнопки button в окне win_obj.
    """
    win = get_win_object(context, win_obj)
    button = win.get_button_by_name(button)
    button.click()
    waitForExtAjax(context)


@step(u'в окне {win_obj} выбрать первую запись таблицы')
def step_select_first_row_from_grid(context, win_obj):
    u"""
    Выбрать первую запись в гриде.
    """
    warn(_DEPRECATION_STEP_STRING)

    eval_el = find_win_obj(context, win_obj)
    context.browser.execute_script("""
    (function find_button_into_toolbar(){
        'use strict';
        var obj = Ext.getCmp('%s');
        var grid = obj.items.items[0].selModel.grid;
        grid.getSelectionModel().selectFirstRow();

        assert(grid.getSelectionModel().hasSelection(), 'Item not selectd');
    })()
    """ % (eval_el[win_obj]['id']))


@step(u'в окне {win_obj} на вкладке {tab_name} выбрать {one_more}'
      u'запись {element} по колонке {column_name}')
@step(u'в окне {win_obj} на вкладке {tab_name} выбрать '
      u'запись {element} по колонке {column_name}')
@step(u'в окне {win_obj} на вкладке {tab_name} можно выбрать '
      u'запись {element} по колонке {column_name}')
def step_find_and_select_row_on_tab(
    context, win_obj, tab_name, element, column_name, one_more=''
):
    u"""
    Выбор записи в гриде.
    """
    warn(_DEPRECATION_STEP_STRING)

    eval_el = find_win_obj(context, win_obj)
    context.browser.execute_script(u"""
        ui.find_and_select_row_on_tab('{0}', '{1}', '{2}', '{3}', '{4}')
    """.format(
        eval_el[win_obj]['id'], tab_name, element, column_name, one_more)
    )


@step(u'в окне {win_obj} с одноколоночными гридами '
      u'выбрать запись {element} по колонке {column_name}')
def step_select_grid_record(context, win_obj, element, column_name):
    u"""
    Выбрать запись в гриде по колонке.
    """
    warn(_DEPRECATION_STEP_STRING)

    eval_el = find_win_obj(context, win_obj)
    window = context.browser.find_element_by_id(eval_el[win_obj]['id'])
    grid_obj = window.find_elements_by_class_name('x-grid-panel')
    grid_obj_ids = [str(grid.get_attribute('id')) for grid in grid_obj]

    context.browser.execute_script(u"""
        ui.find_and_select_row_in_grid({0}, '{1}', '{2}')
    """.format(grid_obj_ids, element, column_name))


@step(u'в окне {win_obj} выбрать {one_more} запись {element} по '
      u'колонке {column_name}')
@step(u'в окне {win_obj} выбрать запись {element} по колонке {column_name}')
@step(u'в окне {win_obj} можно выбрать запись {element} по '
      u'колонке {column_name}')
def step_find_and_select_row(context, win_obj, element, column_name,
                             one_more=''):
    u"""
    Выбрать запись в гриде по колонке.
    """
    warn(_DEPRECATION_STEP_STRING)

    eval_el = find_win_obj(context, win_obj)
    grid_obj = get_toolbar_id_by_column_name(
        context, eval_el[win_obj]['id'], column_name
    )
    if not grid_obj:
        grid_obj = ''

    context.browser.execute_script(u"""
        ui.find_and_select_row('{0}', '{1}', '{2}', '{3}', '{4}')
    """.format(eval_el[win_obj]['id'], grid_obj, element,
               column_name, one_more)
    )


@step(
    u'в древоводином окне {win_obj} выбрать запись '
    u'{elements} по колонке {column_name}'
)
def step_find_and_select_node(context, win_obj, elements, column_name):
    u"""
    Выделяет запись в гриде с древовидной структурой записей.

    (Например как в реестре Учреждение на проекте ЭШ).

    :param context: behave-контекст степа.
    :param win_obj: Название окна.
    :param elements: Имя элемента для выделения. Если элемент является
     дочерним, то имя указывается как перечесление всех элементов в пути
     разделенных знаком ->. Пример: Министерство -> Управление -> Школа будет
     выбран элемент Школа который является дочерним для элемента Управление,
     который в свою очередь является дочерним для элемента Министерство.
    :param column_name: Столбец для поиска грида.
    """
    _find_and_select_node(context, win_obj, elements, column_name)


@step(u'в окне {win_obj} открыть вкладку {tab_name}')
def step_find_and_open_panel(context, win_obj, tab_name):
    u"""
    Открывает вкладку с названием tab_name в окне win_obj

    :param context: behave-контекст степа.
    :param win_obj: Название окна.
    :param tab_name: Название вкладки.
    """
    win = get_win_object(context, win_obj)
    win.open_tab(tab_name)


@step(u'в окне {win_obj} вкладка {tab_name} открыта')
def step_is_tab_opened(context, win_obj, tab_name):
    u"""
    Преверяет открыта ли вкладка с названием tab_name в окне win_obj

    :param context: behave-контекст степа.
    :param win_obj: Название окна.
    :param tab_name: Название вкладки.
    """
    win = get_win_object(context, win_obj)
    assert win.is_tab_open(tab_name)


@step(u'в окне {win_obj} вкладка {tab_name} {status}')
def step_is_tab_active(context, win_obj, tab_name, status):
    u"""
    Преверяет "кликабельность" вкладки с названием tab_name в окне win_obj

    :param context: behave-контекст степа.
    :param win_obj: Название окна.
    :param tab_name: Название вкладки.
    :param status: проверяемый статус вкладки (активна/неактивна).
    """
    win = get_win_object(context, win_obj)
    if status == u'активна':
        assert win.is_tab_active(tab_name)
    elif status == u'неактивна':
        assert not win.is_tab_active(tab_name)


@step(
    u'в Расписании уроков выбрать ячейку на пересечении'
    u' класса {class_name} и дня недели {day} со временем {time}'
)
def step_find_and_select_schedule_record(context, class_name, day, time):
    u"""
    Выбирает ячейку в расписании уроков с заданными параметрами.
    """
    warn(_DEPRECATION_STEP_STRING)
    win_obj = u'Расписание уроков'
    eval_el = find_win_obj(context, win_obj)
    window = context.browser.find_element_by_id(eval_el[win_obj]['id'])
    grid_obj = window.find_element_by_class_name('x-grid-panel')

    context.browser.execute_script(u"""
        ui.find_and_select_row_with_weekday('{0}', '{1}', '{2}', '{3}')
    """.format(grid_obj.get_attribute('id'), class_name, day, time))


# TODO: Сделать два степа с разным набором аргументов, которые вызывают общую
#       функцию.
@step(
    u'в Классном журнале два раза щелкнуть на ячейку'
    u' c датой {date} и временем {time}'
)
@step(
    u'в Классном журнале два раза щелкнуть на ячейку'
    u' c датой {date} и без времени'
)
def step_click_by_journal_cell(context, date, time=''):
    u"""
    Вызов Журнала на урок путем двойного щелчка по дате урока.
    """
    win_obj = u'Классный журнал'
    eval_el = find_win_obj(context, win_obj)
    window = context.browser.find_element_by_id(eval_el[win_obj]['id'])
    grid_obj = window.find_element_by_class_name('x-grid-panel')

    context.browser.execute_script(u"""
            ui.find_and_select_row_date('{0}', '{1}', '{2}')
        """.format(grid_obj.get_attribute('id'), date, time)
    )


@step(u'в Классном журнале щелкнуть на ячейку'
      u' c датой {date} и временем {time}')
@step(u'в Классном журнале щелкнуть на ячейку'
      u' c датой {date} и без времени')
def step_click_by_journal_cell(context, date, time=''):
    u"""
    Вызов Журнала на урок путем щелчка по дате урока.
    """
    button = context.browser.find_element_by_partial_link_text("{0} {1}".format(date, time))
    button.click()


@step(u'в Классном журнале щелкнуть на дату {date} учебного периода временем {time}')
@step(u'в Классном журнале щелкнуть на дату {date} учебного периода без времени')
def step_click_on_date_period(context, date, time=''):
    u"""
    Вызов Журнала на урок путем щелчка по дате урока.
    """
    win_obj = u'Классный журнал'
    eval_el = find_win_obj(context, win_obj)
    window = context.browser.find_element_by_id(eval_el[win_obj]['id'])
    grid_obj = window.find_element_by_class_name('x-grid-panel')

    context.browser.execute_script(u"""
           ui.find_and_select_row_date_link('{0}', '{1}', '{2}')
        """.format(grid_obj.get_attribute('id'), date, time)
    )


@step(
    u'в окне {win_obj} запись с значением {column_value} по колонке '
    u'{column_name} будет удалена'
)
def step_is_record_removed(context, win_obj, column_value, column_name):
    u"""
    Проверка что в гриде нет записи с значение column_value по колонке
    column_name. Степ устаревший, не рекомендуется к использованию.
    """
    eval_el = find_win_obj(context, win_obj)
    toolbar_id = get_toolbar_id_by_column_name(
        context, eval_el[win_obj]['id'], column_name
    )
    record_removed = context.browser.execute_script(u"""
        return ui.is_record_removed('{0}', '{1}', '{2}');
        """.format(toolbar_id, column_name, column_value))
    assert record_removed, "Record not removed"


@step(u'в диалоговом окне {win_obj} нажать кнопку {button_name}')
def step_press_button_on_dlg_win(context, win_obj, button_name):
    u"""
    Нажать кнопку button_name в окне win_obj.

    Если окно без названия, то в качестве названия нужно указать None.

    :param context: behave-контекст степа.
    :param win_obj: Название окна.
    :param button_name: Название кнопки.
    """
    win_id = get_modal_win_id_by_name(context, win_obj)
    win = context.browser.find_element_by_id(win_id)
    button_id = None
    buttons = win.find_elements_by_tag_name('button')
    for button in buttons:
        if button.text == button_name:
            button_id = button.get_attribute('id')
    button = context.browser.find_element_by_id(button_id)
    button.click()


@step(u'в окне {win_obj} есть безколоночный грид "{grid_name}"')
def step_find_grid_with_no_columns(context, win_obj, grid_name):
    win_id = find_win_obj(context, win_obj)[win_obj]['id']
    grid_list = context.browser.find_elements_by_xpath(
        "//div[@id='{0}']"
        "//div[contains(@class, 'x-panel x-box-item')]".format(win_id)
    )

    grid_id = None
    for i in range(len(grid_list)):
        name = grid_list[i].find_element_by_class_name(
            'x-panel-header-text').text
        if name == grid_name:
            grid_id = grid_list[i].get_attribute('id')
            context.win_objects['colmnless_grid_id'] = grid_id
            break

    assert grid_id, 'Columnless grid {0} not found'.format(grid_name)


@step(u'в безколоночном гриде на панели уснструментов есть элемент {element}')
def step_check_element_on_columnless_grid_toolbar(context, element):
    elem_dict = {
        u'Выбора шрифта': 'x-font-select',
        u'Жирного шрифта': 'x-edit-bold',
        u'Наклонного шрифта': 'x-edit-italic',
        u'Подчеркивания шрифта': 'x-edit-underline',
        u'Увеличения размера шрифта': 'x-edit-increasefontsize',
        u'Уменьшения размера шрифта': 'x-edit-decreasefontsize',
        u'Смены цвета шрифта': 'x-edit-forecolor',
        u'Смены фона шрифта': 'x-edit-backcolor',
        u'Выровнять по левому краю': 'x-edit-justifyleft',
        u'Выровнять по центру': 'x-font-select',
        u'Выровнять по правому краю': 'x-font-select',
        u'Вставка гиперссылки': 'x-edit-createlink',
        u'Нумерованый список': 'x-edit-insertorderedlist',
        u'Маркированый список': 'x-edit-insertunorderedlist',
        u'Исходный код': 'x-edit-sourceedit',
    }
    does_exist = False
    grid_id = context.win_objects['colmnless_grid_id']
    elem_list = context.browser.find_elements_by_xpath(
        "//div[@id='{0}']"
        "//div[contains(@class, 'x-html-editor-tb')]"
        "//button".format(grid_id)
    )
    select_elem = context.browser.find_element_by_xpath(
        "//div[@id='{0}']"
        "//div[contains(@class, 'x-html-editor-tb')]"
        "//select".format(grid_id)
    )
    elem_list.append(select_elem)

    for elem in elem_list:
        if elem_dict[element] in elem.get_attribute('class'):
            does_exist = True
            break

    assert does_exist, 'Element {0} not found'.format(element)


@step(u'в окне "{win_obj}" есть кнопка "{button_name}"')
def step_is_button_on_panel(context, win_obj, button_name):
    u"""
    Проверка что в окне есть button_name.

    :param context: behave-контекст степа.
    :param win_obj: Название окна.
    :param button_name: Название кнопки.
    """
    win = get_win_object(context, win_obj)
    assert win.get_button_by_name(button_name), u'Кнопки не существует.'


@step(u'в поле без метки "{field_name}"'
      u' окна {win_obj} внести значение {value}')
def step_set_value(context, field_name, win_obj, value):
    u"""
    Устанавливает значение value в поле у которого не указан label.

    (например поле Поиск).

    :param context: behave-контекст степа.
    :param win_obj: Название окна.
    :param value: Значение для установки в поле.
    :param field_name: Значение которое содержится в поле на момент начала
     выполнения данного шага..
    """
    eval_el = find_win_obj(context, win_obj)
    win = context.browser.find_element_by_id(eval_el[win_obj]['id'])
    input_field = None
    for i in win.find_elements_by_tag_name('input'):
        if i.get_attribute('value') == field_name:
            input_field = i
            break
    input_field.clear()
    input_field.send_keys(value)
    input_field.send_keys(Keys.ENTER)


@step(u'и в окне {win_obj} у поля Поиск нажать кнопку крестик')
def step_press_clear_trigger(context, win_obj):
    u"""
    Закрытие окна путем нажатия кнопки "крестик".
    """
    eval_el = find_win_obj(context, win_obj)
    button = context.browser.find_element_by_xpath(
        "//div[@id='{0}']"
        "//img[contains(@class, 'x-form-trigger x-form-clear-trigger')]"
        "".format(eval_el[win_obj]['id']))
    button.click()


@step(u'нажать ENTER в поле со значением {value} окна {win_obj}')
def step_send_filed(context, value, win_obj):
    u"""
    Фокусирование на поле с значением value и нажатие кнопки ENTER.
    Используется например для заполнения полей поиска.

    :param context: behave-контекст степа.
    :param win_obj: Название окна.
    :param value: Значение для установки в поле.
    """
    eval_el = find_win_obj(context, win_obj)
    win = context.browser.find_element_by_id(eval_el[win_obj]['id'])
    inputs = win.find_elements_by_tag_name('input')
    elem = None
    for i in inputs:
        if i.get_attribute('value') == value:
            elem = i
            break
    context.action.key_down(Keys.ENTER, elem).perform()


@step(u'в гриде окна {win_obj} кликнуть по заголовку {header_name}')
def step_click_by_grid_header(context, win_obj, header_name):
    u"""
    Осуществляет клик по заголовку столбца.

    Используется для сортировки по столбцу.

    :param context: behave-контекст степа.
    :param win_obj: Название окна.
    :param header_name: Название заголовка столбца.
    """
    win = get_win_object(context, win_obj)
    grid = win.get_grid_by_column_header(header_name)
    xpath_grid_headers = (
        u"//div[@id='{id}']"
        u"//*[contains(@class,'x-grid3-hd-inner')]".format(id=grid.grid_id)
    )
    header = None
    for i in grid.driver.find_elements_by_xpath(xpath_grid_headers):
        if i.text == header_name:
            header = i
            break
    header.click()


@step(u'записи в гриде окна {win_obj} будут отсортированы по {sort_type}')
def step_grid_sort(context, win_obj, sort_type):
    u"""
    Проверка что в гриде была произведена сортировка.

    :param context: behave-контекст степа.
    :param win_obj: Название окна.
    :param sort_type: Тип сортировки - по возрастанию или убыванию.
    """
    eval_el = find_win_obj(context, win_obj)
    window = context.browser.find_element_by_id(eval_el[win_obj]['id'])
    grid_obj = window.find_element_by_class_name('x-grid-panel')
    sort_info = context.browser.execute_script(u"""
        return ui.grid_records_sort_info('{0}')
    """.format(grid_obj.get_attribute('id')))
    if sort_type == u'возрастанию':
        assert sort_info['direction'] == u'ASC'
    elif sort_type == u'убыванию':
        assert sort_info['direction'] == u'DESC'


@step(u'в окне {win_obj} у поля {field_label} в выпадающем'
      u' списке будет значение {element}')
def ste_find_record_in_m3_select(context, win_obj, field_label, element):
    u"""
    Проверка того что в выпадающем списке field_label есть значение element.

    :param context: behave-контекст степа.
    :param win_obj: Название окна.
    :param field_label: Название выпадающего списка.
    :param element: Искомое значение.
    """
    eval_el = find_win_obj(context, win_obj)
    input_id = None
    win = context.browser.find_element_by_id(eval_el[win_obj]['id'])
    context.webdriverwait.until(
        lambda driver: driver.find_element_by_xpath(
            "//div[contains(@class, 'x-combo-list-item x-combo-selected')]"
        )
    )
    for i in win.find_elements_by_tag_name('label'):
        if field_label in i.text:
            input_id = i.get_attribute('for')
            break
    record_in_list = context.webdriverwait.until(
        lambda driver: driver.execute_script(u"""
            return ui.is_record_in_dynamic_select('{0}','{1}')
        """.format(input_id, element))
    )
    assert record_in_list, 'Record {} is not in list'.format(element)


@step(u'в окне {win_obj} отображается кнопка {action} файла')
def step_find_file_clear_button(context, win_obj, action):
    u"""
    Проверка что у поля для прикрепления файла отображаются кнопка action.

    :param context: behave-контекст степа.
    :param win_obj: Название окна.
    :param action: Название кнопки может принимать значение 'удаления',
     'прикрепления'.
    """
    eval_el = find_win_obj(context, win_obj)
    win = context.browser.find_element_by_id(eval_el[win_obj]['id'])
    if action == u'удаления':
        assert win.find_element_by_css_selector('.x-form-file-clear')
    else:
        assert win.find_element_by_css_selector('.x-form-file')


@step(u'откроется новая вкладка с заголовком {win_title}')
def step_is_new_tab_open(context, win_title):
    u"""
    Проверка что открылась новая вкладка браузера.
    """
    assert is_tab_with_title_open(context, win_title), "Tab not open"


@step(u'откроется новая вкладка окна {win_obj} с заголовком {tab_name}')
def step_window_tab_open(context, win_obj, tab_name):
    u"""
    Проверка что открылась вкладка окна с заголовком tab_name.
    """
    win = get_win_object(context, win_obj)
    win.open_tab(tab_name)
    assert win.is_tab_open(tab_name), "Tab not open"


@step(u'кнопка {button_name} окна "{win_obj}" {status}')
def step_button_state(context, button_name, win_obj, status):
    u"""
    Проверка что кнопка с названием button_name активна/не активна.

    :param context: behave-контекст степа.
    :param win_obj: Название окна.
    :param button_name: Название кнопки.
    :param status: Статус кнопки - активна/не активна
    """
    win = get_win_object(context, win_obj)
    button = win.get_button_by_name(button_name)
    if status == u'активна':
        assert button.is_enabled(), 'Buttons is not enabled'
    elif status == u'неактива':
        assert not button.is_enabled(), 'Buttons not enabled'


@step(u'ожидаем импорта файла')
def step_wait_import(context):
    u"""
    Ожидание завершения импорта файла.
    """
    waitForImport(context)


@step(u'в окне {win_obj} содержится сообщение "{message}"')
def step_message_in_win(context, win_obj, message):
    u"""
    Проверка того что в окне win_obj отображается сообщение message.
    """
    win = get_win_object(context, win_obj)
    if win:
        text = win.get_text()
    else:
        win_id = get_modal_win_id_by_name(context, win_obj)
        text = context.browser.find_element_by_id(win_id).text
    assert message in text, "Text not in window or not match"


@step(u'в html редакторе, окна {win_obj}, с именем {html_name}'
      u' ввести значение "{value}"')
def step_set_value_in_html_editor(context, win_obj, html_name, value):
    u"""
    Установить значение value в редактор типа wysiwyg
    """
    win = get_win_object(context, win_obj)
    editor = win.get_htmleditor(html_name)
    editor.set_value(value)


@step(u'в html редакторе, окна {win_obj}, с именем {html_name}'
      u' содержится значение "{value}"')
def step_check_value_in_html_editor(context, win_obj, html_name, value):
    win = get_win_object(context, win_obj)
    editor = win.get_htmleditor(html_name)
    assert value in editor.get_value(), "Value don't match"


# TODO: Сделать два степа с разным набором аргументов, которые вызывают общую
#       функцию.
@step(u'в скаченном файле на странице номер {page_num}'
      u' содержится запись "{value}"')
@step(u'в скаченном файле содержится запись "{value}"')
def step_check_record_in_excel(context, value, page_num=1):
    u"""
    Проверка того что в скаченном Excel файле содержится значение value.
    """
    file_name = get_report_file_name(context)
    if not file_name and hasattr(context, 'acd'):
        file_name = context.acd.get('file_name', None)
    assert file_name, u'File not found!'
    file_path = os.path.join(context.settings.MEDIA_ROOT, file_name)
    assert os.path.exists(file_path), (
        u"File {} does not exist".format(file_path)
    )
    rb = xlrd.open_workbook(file_path, formatting_info=True)
    sheet = rb.sheet_by_index(int(page_num) - 1)

    record_in_file = False
    for idx in range(0, sheet.nrows):
        row = sheet.row_values(idx)
        row_string = ' '.join(
            [
                six.text_type(convert_cell_value(sheet.cell(idx, i)))
                for i, x in enumerate(row)
            ]
        )
        record_in_file = value in row_string
        if record_in_file:
            break

    assert record_in_file


@step(u'в окне {win_obj} есть безымянное поле с датой {current_date}')
def step_find_nameless_datefield(context, win_obj, current_date):
    date_field = context.browser.find_element_by_name('date')
    context.win_objects['nameless_date_field'] = date_field
    assert date_field, "Field doesn't exist"
    date_field_value = context.browser.execute_script("""
    var date_field = Ext.getCmp('{0}');
    return date_field.value;
    """.format(date_field.get_attribute('id')))
    assert current_date == date_field_value, "Dates isn't equal"


@step(u'в окне {win_obj} есть безымянное поле с сегодняшней датой')
def step_find_nameless_datefield_with_today_date(context, win_obj):
    date_field = context.browser.find_element_by_name('date')
    context.win_objects['nameless_date_field'] = date_field
    assert date_field, "Field doesn't exist"
    date_field_value = context.browser.execute_script("""
    var date_field = Ext.getCmp('{0}');
    return date_field.value;
    """.format(date_field.get_attribute('id')))
    current_date = datetime.datetime.now()
    assert current_date.strftime("%d.%m.%Y") == date_field_value, "Dates isn't equal"


@step(u'в окне {win_obj} безымянное поле {field} доступно для редактирования')
def step_nameless_field_is_edit(context, win_obj, field):
    if field == u'даты':
        nameless_field = context.win_objects['nameless_date_field']
    else:
        nameless_field = context.win_objects['nameless_filter_field']
    is_edit = context.browser.execute_script("""
    var date_field = Ext.getCmp('{0}');
    return date_field.isEdit;
    """.format(nameless_field.get_attribute('id')))
    assert is_edit, "Field isn't editable"


@step(u'в окне {win_obj} есть безымянное поле фильтра со значением "{value}"')
def step_find_nameless_filter_field(context, win_obj, value):
    eval_el = find_win_obj(context, win_obj)
    win = context.browser.find_element_by_id(eval_el[win_obj]['id'])
    inputs_list = win.find_elements_by_tag_name('input')
    exist = None
    for i in inputs_list:
        if i.get_attribute('value') == value:
            exist = True
            break
    # TODO: Отрефакторить этот степ так, чтобы не было необходимости
    #       использовать переменную i вне тела цикла.
    context.win_objects['nameless_filter_field'] = i
    assert exist


@step(u'в окне {win_obj} нажать по безымянному полю фильтра')
def step_click_nameless_filter_field(context, win_obj):
    filter_field = context.win_objects['nameless_filter_field']
    filter_field.click()
    waitForExtAjax(context)
    items = context.browser.find_elements_by_css_selector(
        ".x-combo-list[style*='visibility: visible;'] .x-combo-list-item")
    context.win_objects['filter_options'] = items


# функция для ЭШ, выше для ЭДО
# TODO объеденить обе функции,
#  чтобы новая функция отрабатывала в двух проектах
# TODO нужно вынести определение филда или элемента в отдельную функцию,
#  так как здесь достаточно много всего повторяется
@step(u'в окне {win_obj} кликнуть по безымянному полю фильтра со значением '
      u'{value}')
def step_click_nameless_filter_field_esch(context, win_obj, value):
    win_id = find_win_obj(context, win_obj)[win_obj]['id']
    win = context.browser.find_element_by_id(win_id)
    fields = win.find_elements_by_tag_name('input')
    field_flag = False
    for field in fields:
        if field.get_attribute('value') == value:
            field.click()
            field_flag = True

    assert field_flag, "Field not found"


@step(u'в выпадающем безымянном списке окна {win_obj} со значением {value} '
      u'будет запись {list_value}')
def step_check_nameless_filter_filed_value_list(
        context, win_obj, value, list_value):
    win_id = find_win_obj(context, win_obj)[win_obj]['id']
    win = context.browser.find_element_by_id(win_id)
    fields = win.find_elements_by_tag_name('input')
    field_flag = False
    list_value_flag = False
    for field in fields:
        if field.get_attribute('value') == value:
            items = context.browser.find_elements_by_css_selector(
                ".x-combo-list[style*='visibility: visible;'] "
                ".x-combo-list-item")
            for i in items:
                if i.text == list_value:
                    list_value_flag = True

            field_flag = True

    assert field_flag, "Field not found"
    assert list_value_flag, "List value not found"


@step(u'в выпадающем безымянном списке окна {win_obj} со значением {value} '
      u'выбрать запись {list_value}')
def step_check_nameless_filter_filed_value_list(
        context, win_obj, value, list_value):
    win_id = find_win_obj(context, win_obj)[win_obj]['id']
    win = context.browser.find_element_by_id(win_id)
    fields = win.find_elements_by_tag_name('input')
    field_flag = False
    list_value_flag = False
    for field in fields:
        if field.get_attribute('value') == value:
            items = context.browser.find_elements_by_css_selector(
                ".x-combo-list[style*='visibility: visible;'] "
                ".x-combo-list-item")
            for i in items:
                if i.text == list_value:
                    i.click()
                    list_value_flag = True

            field_flag = True

    assert field_flag, "Field not found"
    assert list_value_flag, "List value not found"


# TODO подобного рода шаги, где непонятно каким образом берется окно и поле,
#  нужно исправить
@step(u'в выпадающем списке будет значение {value}')
def step_find_value_in_drop_list(context, value):
    items = context.win_objects['filter_options']
    exist = False
    for item in items:
        if item.text == value:
            exist = True
    assert exist


@step(u'в выпадающем списке выбрать пункт "{value}"')
def step_click_item_in_drop_list(context, value):
    items = context.win_objects['filter_options']
    option = None
    for item in items:
        if item.text == value:
            option = item
            break

    assert option, 'Not found option {0}'.format(value)
    option.click()


@step(u'зажать кнопку {key_name}')
def step_hold_key(context, key_name):
    keys_dict = {
        'CTRL': Keys.CONTROL,
        'SHIFT': Keys.SHIFT,
        'ALT': Keys.ALT
    }
    context.action.key_down(keys_dict[key_name]).perform()


@step(u'в окне {win_obj} в странном гриде выбрать запись {value}')
def step_select_row_in_strange_grid(context, win_obj, value):
    win_id = find_win_obj(context, win_obj)[win_obj]['id']
    rows_list = context.browser.find_elements_by_xpath(
        "//div[@id='{0}']"
        "//div[contains(@class, 'x-grid3-cell-inner')]"
        "".format(win_id)
    )
    for row in rows_list:
        if row.text == value:
            row.click()
            break

# TODO: привести к одному виду field_set, fieldset и тд
@step(u'в окне {win_name} есть блок полей с названием {field_set_name}')
def step_check_fields_set_exists(context, win_name, field_set_name):
    u"""
    Проверка наличия блока полей с названием field_set_name в окне win_name.

    :param context: behave-контекст степа.
    :param win_name: Название окна.
    :param field_set_name: Название поля.
    """
    win = get_win_object(context, win_name)
    assert win.get_fieldset_by_name(field_set_name), (
        u"Fieldset name not found.")

# TODO: убрать из-за странной формулировки
@step(u'{action} в окне {win_obj} блок полей {fieldset}')
def step_open_fieldset(context, action, win_obj, fieldset):
    win = get_win_object(context, win_obj)
    fs = win.get_fieldset_by_name(fieldset)
    fs.click()


@step(u'в окне {win_obj} развернуть блок {field_set}')
def step_expand(context, win_obj, field_set):
    win = get_win_object(context, win_obj)
    fs = win.get_fieldset_by_name(field_set)
    fs.click()


@step(u'блок {field_set} окна {win_obj} {collapsed}')
@step(u'блок {field_set} окна "{win_obj}" {collapsed}')
def step_check_fieldset_is_collapsed(context, field_set, win_obj, collapsed):
    win = get_win_object(context, win_obj)
    fs = win.get_fieldset_by_name(field_set)
    if collapsed == u'свернут':
        assert fs.is_collapsed()
    else:
        assert not fs.is_collapsed()


@step(u'в окне {win_obj} есть поле вильтрации в колонке {col_name}')
def step_check_filter(context, win_obj, col_name):
    column_filter_args = {
        u'Учреждение': 'filter_1',
        u'Дата': ['filter_2', 'filter_3'],
        u'Мероприятие': 'filter_4'
    }
    win_id = find_win_obj(context, win_obj)[win_obj]['id']
    arg_name = column_filter_args[col_name]
    if type(arg_name) is list:
        for name in arg_name:
            filter_field = context.browser.find_element_by_xpath(
                "//div[@id='{0}']"
                "//input[@name='{1}']".format(win_id, name)
            )
            assert filter_field
    else:
        filter_field = context.browser.find_element_by_xpath(
            "//div[@id='{0}']"
            "//input[@name='{1}']".format(win_id, arg_name)
        )
        assert filter_field


@step(u'в окне {win_obj} в поле фильтра "{filter_name}"'
      u' установить значение {record}')
def step_input_filter_record(context, win_obj, filter_name, record):
    filter_dict = {
        u'Учреждение': 'filter_1',
        u'Дата с': 'filter_2',
        u'Дата по': 'filter_3',
        u'Мероприятие': 'filter_4',
    }

    win_id = find_win_obj(context, win_obj)[win_obj]['id']
    arg_name = filter_dict[filter_name]
    filter_field = context.browser.find_element_by_xpath(
        "//div[@id='{0}']"
        "//input[@name='{1}']".format(win_id, arg_name)
    )

    filter_field.click()
    filter_field.clear()
    filter_field.send_keys(record)
    filter_field.send_keys(Keys.ENTER)


@step(u'кликнуть по появившемуся выпадающему списку')
def step_select_current_record_in_select_list(context):
    select = context.browser.find_element_by_id(
        context.win_objects['editor_id'])
    select.click()


@step(u'в {window_title} доступна кнопка {button_name}')
def step_wait_grid_load(context, window_title, button_name):
    u"""
    Ждем появления грида путем проверки доступности его кнопки на grid panel.

    Используется для ожидания загрузки гридов которые изначально не были на
    странице, а подгружаются по наступлению какого-либо события.
    (Например журнал для выставление оценок в окне Классный журнал).
    """
    win = get_win_object(context, window_title)
    context.webdriverwait.until(
        lambda driver: driver.find_element_by_xpath(u"""
            //div[@id='{win_id}']//button[text()='{b_name}']
        """.format(win_id=win.win_id, b_name=button_name))
    )


@step(
    u'в древовидном окне {win_obj} элемент {elements} по колонке'
    u' {column_name} не имеет дочерних записей'
)
def element_is_leaf(context, win_obj, elements, column_name):
    parse_elements = [x.strip() for x in elements.split('->')]
    eval_el = find_win_obj(context, win_obj)

    _find_and_select_node(context, win_obj, elements, column_name)

    js_line = u'return ui.element_is_last(\'{0}\', [\'{1}\'], \'{2}\');'.format(
        eval_el[win_obj]['id'],
        "', '".join(parse_elements),
        column_name
    )
    context.webdriverwait.until(lambda driver: driver.execute_script(js_line))

    is_leaf = context.browser.execute_script(u"""
        return ui.element_is_leaf('{}')
    """.format(eval_el[win_obj]['id']))

    assert is_leaf, u'У элемента имеются дочерние записи.'


@step(u'перезагрузить страницу')
def step_refresh_page(context):
    context.browser.refresh()


@step(u'выполнить ПКМ')
def step_mouse_right_button_click(context):
    u"""
    Осуществляет правый клик мышью на текущей позиции курсора в окне
    :param context:
    """
    ActionChains(context.browser).context_click().perform()


@step(u'в окне {win_name} содержатся вкладки {panel_names}')
def step_check_win_panels(context, win_name, panel_names):
    u"""
    Проверка количества вкладок в окне и их названий.
    """
    need_compare = True
    win = get_win_object(context, win_name)
    win_panels = context.browser.execute_script(
        u"return win_helpers.get_win_panels('{}')".format(win.win_id)
    )
    if panel_names == u'None':
        panels = []
        need_compare = False
    else:
        panels = [p_name.strip() for p_name in panel_names.split(',')]
    try:
        _ = win_panels['x-panel-tbar']
        idx = 'x-panel-tbar'
    except KeyError:
        idx = 'x-grid-panel'
    assert len(panels) == len(win_panels[idx]), "Count of tab isn't equal"

    if need_compare:
        for panel in panels:
            assert panel in win_panels[idx], "Tab isn't in current window"


@step(u'в окне {win_name} не содержится блок полей {fieldset_name}')
def step_check_absent_fieldset(context, win_name, fieldset_name):
    u"""
    Проверка отсутствия блока полей(fieldset) в окне.
    """
    win = get_win_object(context, win_name)
    win_fieldsets = context.browser.execute_script(
        u"return win_helpers.get_win_panels('{}')".format(win.win_id)
    )['x-fieldset-tbar']

    assert fieldset_name not in win_fieldsets, "Fieldset is in current window"


@step(u'в окне "{win_name}" нажать ссылку "{link_text}" для скачивания файла')
def step_click_link_for_download(context, win_name, link_text):
    u"""
    Шаг для скачивания файла по ссылке.

    :param context:  behave переменная для передачи данных между шагами,
    передается во все степы первым аргументом.
    :param win_name: Имя окна, в данном шаге используем только для того
    чтобы было понятно в каком окне нажимаем ссылку.
    :param link_text: Текст ссылки, необходим для ее поиска.
    """
    link = context.browser.find_element_by_xpath(u"""
        //a[text()='{}']
    """.format(link_text))
    assert link, u'Link not found!'
    link.click()
    link_path = link.get_attribute('href')

    if not hasattr(context, 'acd'):
        context.acd = {}

    context.acd.update(
        file_name=link_path.split('/')[-1]
    )


@step(u'заполнить поля в окне "{win}"')
def step_fil_win_fields(context, win):
    win = get_win_object(context, win)
    for row in context.table:
        field = win.get_field_by_name(row['name'])
        if row['type'] in ('text', 'date'):
            field.set_value(row['value'])
        elif row['type'] == 'select':
            field.click_by_trigger(u'выпадающего списка')
            waitForExtAjax(context)
            field.select_combobox_item(row['value'])
        elif row['type'] == 'autocomplete':
            field.set_value(row['value'])
            context.webdriverwait.until(
                lambda d: d.execute_script(u"""
                        var f = Ext.getCmp('{0}');
                        var l = document.getElementById(f.list.id);
                        return l.style['visibility'] == 'visible';
                    """.format(field.field_id))
                )
            field.select_combobox_item(row['actual_value'])


@step(u'в окне {win_obj} кнопка {btn} не активна')
def button_active(context, win_obj, btn):
    win = get_win_object(context, win_obj)
    id_button = win.get_atr_btn(btn)
    element_disabled = context.browser.execute_script(u"""
                        var f = Ext.getCmp('{0}');
                        f.disabled;
                        return f.disabled;
                    """.format(id_button))
    assert element_disabled
