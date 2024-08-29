# -*- coding: utf-8 -*-
u"""
Набор степов для работы с гридами.
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import numbers
import parse

from behave import step
from behave import register_type
from parse_type import TypeBuilder

from .helpers import editor_input_value
from .winobject import GridContextMenu
from .winobject import GridNotFound
from .winobject import get_win_object
import six


@parse.with_pattern(r"не\s+")
def parse_in(text):
    return text.strip()

parse_optional_in = TypeBuilder.with_optional(parse_in)
register_type(optional_in_=parse_optional_in)


@step(u'в гриде со столбцом "{column_name}" на вкладке {panel}'
      u' окна {win_name} выбрать запись {value}')
@step(u'в гриде со столбцом "{column_name}" окна {win_name}'
      u' выбрать запись {value}')
@step(u'в гриде со столбцами "{columns}" окна {win_name}'
      u' выбрать запись {value} по столбцу {column_name}')
def step_find_and_select_row(context, column_name, win_name,
                             value, panel=None, columns=None):
    u"""
    Выбор записи в гриде.

    :param column_name: Название столбца по которому будет найден грид
    :param value: Значение записи по столбцу column_name. на основе этого
     значение будет найдена запись.
    :param win_name: Название окна в котором расположен грид.
    :param panel: Название вкладки окна на которой расположен грид
    """
    win = get_win_object(context, win_name)
    if panel:
        grid = win.get_grid_by_parent_panel_and_column_header(
            panel,
            column_name
        )
    elif columns:
        grid = win.get_grid_by_column_list(columns)
    else:
        grid = win.get_grid_by_column_header(column_name)
    grid.select_row_by_column_value(column_name, value)


@step(u'в окне "{win_name}" у столбца "{column}" в выпадающем списке'
      u' выбрать запись "{record}"')
def step_select_record_in_column_combobox(context, win_name, column, record):
    u"""
    Выбор записи из выпадающего списка в столбце грида.

    :param win_name: Название окна в котором расположен грид.
    :param column: Название столбца в котором расположен выпадающий список
    :param record: Запись которая будет выбрана.
    """
    win = get_win_object(context, win_name)
    grid = win.get_grid_by_column_header(column)
    grid.select_combobox_item(column, record)


@step(u'в окне "{win_name}" у столбца "{column}" в выпадающем '
      u'списке будет запись "{record}"')
def step_is_record_in_column_combobox(context, win_name, column, record):
    u"""
    Проверка того что record содержится в выпадающем списке столбца column.

    :param win_name: Название окна в котором расположен грид.
    :param column: Название столбца в котором расположен выпадающий список
    :param record: Искомая запись.
    """
    win = get_win_object(context, win_name)
    grid = win.get_grid_by_column_header(column)
    assert record in grid.get_column_list_items(column), 'Record not in list'


@step(u'в окне {win_name} у столбца {column} содержится промежуточное'
      u' значение {record}')
def step_check_cell_tmp_value(context, win_name, column, record):
    win = get_win_object(context, win_name)
    grid = win.get_grid_by_column_header(column)
    assert editor_input_value(
        grid.driver, grid.columns[column]['editorId']
    ) == record, "Record not in column"


@step(u'в окне {win_name} на панели инструментов со столбцом {column} '
      u'нажать кнопку {button_name}')
@step(u'в окне {win_name} на панели инструментов со столбцом {column} '
      u'на вкладке {panel} нажать кнопку {button_name}')
def step_pres_button_on_panel(context, win_name, column, button_name,
                              panel=None):
    u"""
    Deprecated - лучше использовать step_click_grid_button.
    """
    if panel:
        context.execute_steps(u'Если в гриде со столбцом "{column}"'
                              u' на вкладке {panel} окна {win_name}'
                              u' нажать кнопку {button}'.
                              format(column=column, panel=panel,
                                     win_name=win_name, button=button_name))
    else:
        context.execute_steps(u'Если в гриде со столбцом "{column}"'
                              u' окна {win_name} нажать кнопку {button}'.
                              format(column=column, win_name=win_name,
                                     button=button_name))


@step(u'в окне {win_name} на панели инструментов грида со столбцом {column}'
      u' есть кнопка "{button_name}"')
@step(u'в окне {win_name} на панели инструментов грида со столбцом {column}'
      u' на вкладке {panel} есть кнопка "{button_name}"')
@step(u'в окне {win_name} на панели инструментов грида со столбцом {column}'
      u' "{is_absent}" кнопка "{button_name}"')
def step_is_button_on_panel(context, win_name, column, button_name,
                            is_absent=None, panel=None):
    u"""
    Проверка что кнопка button_name есть на панели иснтруметов грида.

    :param win_name: Название окна в котором расположен грид.
    :param column: Название столбца по которому будет найдем нужный грид.
    :param button_name: Искомая кнопка.
    :param panel: Название вкладки окна на которой расположен грид
    """
    win = get_win_object(context, win_name)
    if panel:
        grid = win.get_grid_by_parent_panel_and_column_header(panel, column)
    else:
        grid = win.get_grid_by_column_header(column)
    if not is_absent:
        assert grid.grid_panels['control'].is_button_exist(button_name), (
            "Button not found"
        )
    else:
        assert not grid.grid_panels['control'].is_button_exist(button_name), (
            'Button exist')


@step(u'в гриде со столбцом {column} окна {win_name}'
      u' будет {records_amount} запись')
@step(u'в гриде со столбцом {column} окна {win_name}'
      u' будет {records_amount} записей')
def step_test_win_records_amount(context, column, win_name, records_amount):
    u"""
    Проверка того что в гриде содержится records_amount записей.

    :param win_name: Название окна в котором расположен грид.
    :param column: Название столбца по которому будет найдем нужный грид.
    :param records_amount: Ожидаемое кол-во записей.
    """
    win = get_win_object(context, win_name)
    grid = win.get_grid_by_column_header(column)
    assert grid.get_total_rows_len() == int(records_amount)


@step(u'в гриде со столбцом {column} окна {win_obj} нет записей')
def step_is_grid_empty(context, column, win_obj):
    u"""
    Проверка того что в гриде со столбцом column нет ни одной записи.

    :param win_obj: Название окна в котором расположен грид.
    :param column: Название столбца по которому будет найдем нужный грид.
    """
    win = get_win_object(context, win_obj)
    grid = win.get_grid_by_column_header(column)
    assert len(grid.get_rows()) == 0, 'Grid have records'


@step(u'в окне {win_name} выбрать все записи по колонке {column}')
@step(u'в окне {win_name} на вкладке {panel} '
      u'выбрать все записи по колонке {column}')
def step_select_all_rows_in_grid(context, win_name, column, panel=None):
    u"""
    Выбор всех записей в гриде.

    :param win_name: Название окна в котором расположен грид.
    :param column: Название столбца по которому будет найдем нужный грид.
    :param panel: Название вкладки окна на которой расположен грид.
    """
    win = get_win_object(context, win_name)
    if panel:
        grid = win.get_grid_by_parent_panel_and_column_header(panel, column)
    else:
        grid = win.get_grid_by_column_header(column)
    grid.select_all_rows()


@step(u'все записи грида со столбцом {column}'
      u' окна "{win_name}" {status} признак выделения')
def step_is_all_row_selected(context, column, win_name, status):
    u"""
    Проверка того что все записи грида выбраны/не выбраны.

    :param win_name: Название окна в котором расположен грид.
    :param column Название столбца по которому будет найдем нужный грид.
    :param status:.
    """
    win = get_win_object(context, win_name)
    grid = win.get_grid_by_column_header(column)
    if status == u'имеют':
        assert grid.is_all_rows_selected(), 'Rows not selected'
    elif status == u'не имеют':
        assert not grid.is_all_rows_selected(), 'Rows selected'


@step(u'запись {record} грида со столбцом {column}'
      u' окна "{win_name}" {status} признак выделения')
def step_is_record_selected(context, record, column, win_name, status):
    u"""
    Проверка того что запись record грида выбраны/не выбраны.

    :param win_name: Название окна в котором расположен грид.
    :param column: Название столбца по которому будет найдем нужный грид.
    :param record: Искомая запись.
    """
    win = get_win_object(context, win_name)
    grid = win.get_grid_by_column_header(column)
    if status == u'имеет':
        assert grid.is_row_selected(column, record), 'Rows not selected'
    elif status == u'не имеет':
        assert not grid.is_row_selected(column, record), 'Rows selected'


@step(u'в гриде со столбцом "{column}" окна {win_obj} нажать кнопку {button}')
@step(u'в гриде с названием "{name}" окна {win_obj} нажать кнопку {button}')
@step(u'в гриде со столбцом "{column}" на вкладке {panel}'
      u' окна {win_obj} нажать кнопку {button}')
@step(u'в гриде со столбцами "{columns}" окна {win_obj}'
      u' нажать кнопку {button}')
def step_click_grid_button(context, win_obj, button, column='', panel='',
                           columns=None, name=None):
    u"""
    Производит нажатие на кнопку button на панели управление грида.

    :param win_obj: Название окна в котором расположен грид.
    :param column: Название столбца по которому будет найдем нужный грид.
    :param button: Название кнопки.
    """
    win = get_win_object(context, win_obj)
    if panel:
        grid = win.get_grid_by_parent_panel_and_column_header(panel, column)
    elif columns:
        grid = win.get_grid_by_column_list(columns)
    elif name:
        grid = win.get_grid_by_title(name)
    else:
        grid = win.get_grid_by_column_header(column)
    grid.grid_panels['control'].press_button(button)


@step(u'в гриде на вкладке {panel} окна "{win_name}" {status}'
      u' значение {value} по колонке {column}')
@step(u'в гриде окна "{win_name}" {status} значение {value}'
      u' по колонке {column}')
@step(u'в гриде со столбцами {columns} окна "{win_name}" {status} значение'
      u' {value} по колонке {column}')
@step(u'в гриде с кнопкой {button} окна'
      u' "{win_name}" {status} значение {value}')
def step_check_value_in_grid_rows(context, win_name, value, status, column='',
                                  panel='', columns=None, button=None):
    u"""
    Проверка того что в столбце column содержится/не содержится значение value.

    :param win_name: Название окна в котором расположен грид.
    :param column: Название столбца по которому будет найдем нужный грид.
    :param value: Искомое значение.
    :param panel: Название вкладки окна на которой расположен грид.
    """
    win = get_win_object(context, win_name)
    if panel:
        grid = win.get_grid_by_parent_panel_and_column_header(panel, column)
    elif columns:
        grid = win.get_grid_by_column_list(columns)
    elif button:
        grid = win.get_grid_by_button_name(button)
    else:
        grid = win.get_grid_by_column_header(column)
    val_in_row = False
    for row in grid.get_rows():
        row_val = row[grid.columns[column]['dataIndex']]
        if type(row_val) in (str, six.text_type):
            if value in row_val:
                val_in_row = True
                break
        if isinstance(row_val, numbers.Number):
            if float(value) == row_val:
                val_in_row = True
                break
    if status == u'содержится':
        assert val_in_row, u"Value not in row"
    elif status == u'не содержится':
        assert not val_in_row, u"Value {} in row".format(value)


@step(u'в гриде окна "{win_name}" {status} значение "{value}" в столбце'
      u' "{column}" для строки с значением "{help_column}"'
      u' по столбцу "{help_value}"')
def step_check_value_in_row(context, win_name, status, value, column,
                            help_column, help_value):
    u"""
    Проверка того что для заданной строки грида в столбце column
    содержится/не содержится значение value.

    :param win_name: Название окна в котором расположен грид.
    :param column: Название столбца по которому будет найдем нужный грид.
    :param value: Искомое значение.
    """
    win = get_win_object(context, win_name)
    grid = win.get_grid_by_column_header(column)
    row = grid.get_row_by_column_value(help_column, help_value)
    column_index = grid.columns[column]['dataIndex']
    if status == u'содержится':
        assert six.text_type(row[column_index]) == value, (
            u"Expected {0} but found {1}".format(value, row[column_index])
        )
    elif status == u'не содержится':
        assert six.text_type(row[column_index]) != value, (
            u"Value {0} in row but shouldn't.".format(value, row[column_index])
        )


@step(u'в гриде на вкладке {panel} окна {win_name} кликнуть'
      u' по ячейке с содержимым {value} по колонке {column}')
@step(u'в гриде окна {win_name} кликнуть '
      u'по ячейке с содержимым {value} по колонке {column}')
def step_click_on_grid_cell(context, win_name, value, column, panel=None):
    u"""
    Кликнуть по ячейке со значением value.

    :param win_name: Название окна в котором расположен грид.
    :param column: Название столбца по которому будет найдем нужный грид.
    :param value: Искомое значение.
    :param panel: Название вкладки окна на которой расположен грид.
    """
    win = get_win_object(context, win_name)
    if panel:
        grid = win.get_grid_by_parent_panel_and_column_header(panel, column)
    else:
        grid = win.get_grid_by_column_header(column)
    grid.click_by_row_value(column, value)


@step(u'в гриде со столбцом "{column}" на вкладке {panel} окна {win_name}'
      u' снять выделение со всех строк')
@step(u'в гриде со столбцом "{column}" окна {win_name}'
      u' снять выделение со всех строк')
def step_clear_selection(context, column, win_name, panel=None):
    u"""
    Снять выделение со всех строк в гриде.

    :param win_name: Название окна в котором расположен грид.
    :param column: Название столбца по которому будет найдем нужный грид.
    :param panel: Название вкладки окна на которой расположен грид.
    """
    win = get_win_object(context, win_name)
    if panel:
        grid = win.get_grid_by_parent_panel_and_column_header(panel, column)
    else:
        grid = win.get_grid_by_column_header(column)
    grid.clear_selection()


@step(u'в гриде окна {win_name} выбрать ячейку по столбцу {target_column}'
      u' в строке со значением {row_value} в столбце {help_column}')
@step(u'в гриде на вкладке {panel} окна {win_name} выбрать ячейку по столбцу'
      u' {target_column} в строке со значением {row_value}'
      u' в столбце {help_column}')
def step_select_grid_cell(context, win_name, target_column,
                          row_value, help_column, panel=None):
    u"""
    Выделить ячейку со значением.

    :param win_name: Название окна в котором расположен грид.
    :param target_column: Название столбца в котором будет выбрана ячейка
    :param help_column: Название столбца для поиска грида.
    :param panel: Название вкладки окна на которой расположен грид.
    """
    win = get_win_object(context, win_name)
    if panel:
        grid = win.get_grid_by_parent_panel_and_column_header(panel,
                                                              target_column)
    else:
        grid = win.get_grid_by_column_header(target_column)
    grid.select_cell_by_row_value(target_column, row_value, help_column)


@step(u'в гриде на вкладке {panel} окна {win_obj} установить значение {value} '
      u'в столбце {column} для строки со значением {row_value}'
      u' по столбцу {help_column}')
@step(u'в гриде окна {win_obj} установить значение {value} '
      u'в столбце {column} для строки со значением {row_value}'
      u' по столбцу {help_column}')
def step_set_val_in_cell(context, win_obj, value, column, row_value,
                         help_column, panel=None):
    u"""
    Устанавливает значение value в столбец грида.

    :param win_obj: Название окна в котором расположен грид.
    :param column: Столбец в который будет установлено значение.
    :param help_column: Название столбца для поиска грида.
    :param row_value: Значение столбца help_column необходимое
     для поиска грида.
    """
    win = get_win_object(context, win_obj)
    if panel:
        grid = win.get_grid_by_parent_panel_and_column_header(panel,
                                                              column)
    else:
        grid = win.get_grid_by_column_header(column)
    grid.set_value_in_cell(column, value, help_column, row_value)


@step(u'в гриде на вкладке {panel} окна {win_obj}'
      u' в столбце {column} для строки со значением {row_value}'
      u' по столбцу {help_column} содержится значение {value}')
@step(u'в гриде окна {win_obj} в столбце {column} для строки'
      u' со значением {row_value} по столбцу {help_column}'
      u' содержится значение {value}')
def step_check_cell_value(context, win_obj, value, column, row_value,
                          help_column, panel=None):
    u"""
    Проверяет что в столбце грида установлено значение value

    :param win_obj: Название окна в котором расположен грид.
    :param column: Столбец в который будет установлено значение.
    :param help_column: Название столбца для поиска грида.
    :param row_value: Значение столбца help_column необходимое
     для поиска грида.
    """
    win = get_win_object(context, win_obj)
    if panel:
        grid = win.get_grid_by_parent_panel_and_column_header(panel,
                                                              column)
    else:
        grid = win.get_grid_by_column_header(column)
    actual_value = grid.get_cell_value(column, row_value, help_column)
    if isinstance(actual_value, numbers.Number):
        actual_value = str(actual_value)
    assert actual_value == value, (
        "Valued don't match. Expected {0} but found {1}".format(
            value, actual_value
        )
    )


@step(u'в гриде со столбцом {column} окна'
      u' {win_name} кликнуть по выделенной ячейке')
@step(u'в гриде со столбцом {column} окна'
      u' {win_name} кликнуть по выделенной ячейке в колонке {help_column}')
@step(u'в гриде со столбцом {column} на вкладке {panel} окна'
      u' {win_name} кликнуть по выделенной ячейке')
def step_click_by_selected_cell(context, column, win_name,
                                panel=None, help_column=None):
    u"""
    Кликнуть по выделенной ячейке.

    :param win_name: Название окна в котором расположен грид.
    :param column: Название столбца для поиска грида.
    :param panel: Название вкладки окна на которой расположен грид.
    """
    win = get_win_object(context, win_name)
    if panel:
        grid = win.get_grid_by_parent_panel_and_column_header(panel, column)
    else:
        grid = win.get_grid_by_column_header(column)
    if help_column:
        grid.click_by_selected_cell(help_column)
        editor_id = grid.get_editor_id(help_column)
        context.win_objects['editor_id'] = editor_id
        assert editor_id
    else:
        grid.click_by_selected_cell()


@step(u'ячейка по столбцу {target_column} в гриде со строкой {row_value}'
      u' в столбце {help_column} окна {win_obj} доступна для редактирования')
def step_cell_is_editable(context, target_column, row_value,
                          help_column, win_obj):
    U"""
    Проверка того что ячейка грдида доступна для редактирования
    """
    win = get_win_object(context, win_obj)
    grid = win.get_grid_by_column_header(target_column)
    grid.set_value_in_active_cell(target_column, '42')
    assert grid.get_cell_value(target_column, row_value, help_column) == '42'


@step(u'панель грида со столбцом "{column}" на вкладке "{panel}"'
      u' окна "{win_obj}" {status}')
@step(u'в окне "{win_obj}" панель грида со столбцом "{column}" {status}')
def step_check_grid_panel(context, column, win_obj, status, panel=''):
    u"""
    Проверка активна ли панель инструментов грида.
    """
    win = get_win_object(context, win_obj)
    if panel:
        grid = win.get_grid_by_parent_panel_and_column_header(panel, column)
    else:
        grid = win.get_grid_by_column_header(column)
    panel = grid.grid_panels['control']
    if status == u'активна':
        assert panel.is_enabled(), 'Panel is not enabled'
    elif status == u'неактива':
        assert not panel.is_enabled(), 'Panel not enabled'


@step(u'в окне "{win_obj}" кнопка {button} на панели грида со столбцом'
      u' "{column}" {status}')
def step_grid_button_status(context, win_obj, button, column, status):
    u"""
    Проверка активна ли кнопка на панели инструментов грида.
    """
    win = get_win_object(context, win_obj)
    grid = win.get_grid_by_column_header(column)
    if status == u'активна':
        assert grid.grid_panels['control'].is_button_enabled(button),\
            'Button is not enabled'
    elif status == u'неактива':
        assert not grid.grid_panels['control'].is_button_enabled(button),\
            'Button not enabled'


@step(u'в окне "{win_obj}" грид со столбцом "{column}" {status}')
def step_check_grid_panel(context, column, win_obj, status, panel=''):
    u"""
    Проверка активен ли грид.
    """
    win = get_win_object(context, win_obj)
    if panel:
        grid = win.get_grid_by_parent_panel_and_column_header(panel, column)
    else:
        grid = win.get_grid_by_column_header(column)
    if status == u'активен':
        assert grid.is_enabled(), 'Panel is not enabled'
    elif status == u'неактивен':
        assert not grid.is_enabled(), 'Panel not enabled'


@step(u'в гриде со столбцом {column} окна {win_obj} нажать'
      u' {page_direction} страница')
def step_grid_page_scroll(context, column, win_obj, page_direction):
    u"""
    Переключение страниц в гриде.
    """
    win = get_win_object(context, win_obj)
    grid = win.get_grid_by_column_header(column)
    if page_direction == u'следующая':
        grid.next_page()
    elif page_direction == u'предыдущая':
        grid.prev_page()


@step(u'у всех записей грида окна {win_obj} по колонке'
      u' {column} стоит значение {value}')
def step_check_column_val_for_all_rows(context, win_obj, column, value):
    u"""
    Проверка того, что у всех записей грида в столбце column стоит значение
    value.

    :param win_obj: Название окна в котором расположен грид.
    :param column: Название столбца для поиска грида.
    :param value: Проверяемое значение.
    """
    win = get_win_object(context, win_obj)
    grid = win.get_grid_by_column_header(column)
    col_idx = grid.columns[column]['dataIndex']
    value_in_all_rows = True
    for r in grid.get_rows():
        if value not in r[col_idx]:
            value_in_all_rows = False
    assert value_in_all_rows, 'Value not in all rows'


@step(u'в гриде окна {win_obj} со столбцом {help_column} "{status}"'
      u' {target_column}')
def step_check_column_in_grid(context, win_obj, help_column, status,
                              target_column):
    u"""
    Проверка того, что гриде есть/нет столбец target_column.

    :param win_obj: Название окна в котором расположен грид.
    :param help_column: Вспомогательный столбце для поиска грида.
    :param target_column: Проверяемый столбец.
    :param status: Одна из фраз (есть столбец, нет столбца) указывающих
     тип проверки.
    """
    win = get_win_object(context, win_obj)
    grid = win.get_grid_by_column_header(help_column)
    if status == u'есть столбец':
        assert target_column in grid.columns, 'Column not exist'
    elif status == u'нет столбца':
        assert target_column not in grid.columns, 'Column exist'


@step(u'в гриде окна {win_obj} в строке со значением {value}'
      u' по колонке {column} кликнуть по чекбоксу')
def step_click_grid_checbox(context, win_obj, value, column):
    u"""
    Включает/выключает чекбокс расположенные в столбце column.

    :param win_obj: Название окна в котором расположен грид.
    :param column: Вспомогательный столбце для поиска грида.
    :param value: Значение для поиска необходимой строки.
    """
    win = get_win_object(context, win_obj)
    grid = win.get_grid_by_column_header(column)

    column_key = None
    for row in grid.get_rows():
        for k, v in six.iteritems(row):
            if v == value:
                column_key = k
    assert column_key, u'Column key not found!'
    data_index = grid.columns[column]['dataIndex']

    context.browser.execute_script(u"""
        var grid = Ext.getCmp('{0}');
        var el_id = grid.store.find('{2}', '{1}');
        var rec = grid.store.getAt(el_id);
        rec.set('{3}', 'true')
    """.format(grid.grid_id, value, column_key, data_index))


@step(u'в таблице окна {win_obj} останутся записи со сменой "{value}"')
def step_find_filtered_values(context, win_obj, value):
    win = get_win_object(context, win_obj)
    grid = win.get_grid_by_column_header(u'Урок')
    rows = grid.get_rows()
    another_record = False
    for row in rows:
        if value not in row['weekday']:
            another_record = True
    assert not another_record


@step(u'в гриде со столбцом {column} окна {win_obj}'
      u' кликнуть по строке с значение {row_value}')
def step_click_by_grid_row(context, column, win_obj, row_value):
    u"""
    Клик по строке с значением row_value.

    :param win_obj: Название окна в котором расположен грид.
    :param column: Вспомогательный столбце для поиска грида.
    :param row_value: Значение строки необходимое для ее поиска.
    """
    win = get_win_object(context, win_obj)
    grid = win.get_grid_by_column_header(column)
    grid.click_by_row(row_value)


@step(u'в контекстном меню нажать кнопку "{button_name}"')
def step_click_by_button_name(context, button_name):
    u"""
    Нажатие кнопки button_name в контесктом меню грида. Предварительно
    необходимо открыть меню путем выбора записи в гриде и правого клика мышкой.

    :param context:
    :param button_name:
    :return:
    """
    cm = GridContextMenu.get_visible_menu(context.browser)
    cm.click_by_button(button_name)


@step(u'в гриде с колонкой {column_name} окна {win_name} '
      u'содержатся вкладки {panel_names}')
def step_check_grid_panels(context, win_name, column_name, panel_names):
    u"""
    Проверка количества вкладок гридов окна и их названий
    """
    win = get_win_object(context, win_name)
    grid_panels = context.browser.execute_script(
        u"return win_helpers.get_win_panels('{}')".format(win.win_id)
    )['x-grid-panel']
    panels = [p_name.strip() for p_name in panel_names.split(',')]
    assert len(panels) == len(grid_panels), (
        "Count of tab isn't equal"
    )
    for panel in panels:
        assert panel in grid_panels, (
            "Tab isn't in current grid"
        )


@step(u'в окне {win_name} нет грида с название {grid_name}')
def step_check_grid_is_absent(context, win_name, grid_name):
    u"""
    Проверка отсутствия грида в окне.
    """
    win = get_win_object(context, win_name)
    is_exist = True
    try:
        grid = win.get_grid_by_title(grid_name)
    except GridNotFound:
        is_exist = False
    assert not is_exist, "Grid is exist"


@step(u'в гриде со столбцом "{column}" окна "{win_name}" '
      u'{condition:optional_in_}содержится строка "{test_row}"')
@step(u'в гриде на вкладке "{panel}" со столбцом "{column}" окна "{win_name}" '
      u'{condition:optional_in_}содержится строка "{test_row}"')
@step(u'в гриде с названием "{name}" окна "{win_name}" '
      u'{condition:optional_in_}содержится строка "{test_row}"')
def step_check_row_in_grid(context, win_name, condition,
                           test_row, **kwargs):
    u"""
    Проверка наличия/отсутствия строки в гриде
    :param context: behave context
    :param win_name: Название окна.
    :param condition: Опциональная частица 'не' для проверки того, 
    что строки нет в гриде
    :param test_row: Проверяемая строка 
    :param kwargs: Вспомогательные параметры для локации грида.
    """
    win = get_win_object(context, win_name)
    if kwargs.get('panel') and kwargs.get('column'):
        grid = win.get_grid_by_parent_panel_and_column_header(
            kwargs.get('panel'), kwargs.get('column'))
    elif kwargs.get('name'):
        grid = win.get_grid_by_title(kwargs.get('name'))
    else:
        grid = win.get_grid_by_column_header(kwargs.get('column'))
    grid_rows = [r['row'] for r in grid.get_rows()]
    if condition and condition == u'не':
        assert test_row not in grid_rows, u"Row in grid."
    else:
        assert test_row in grid_rows, u"Row not in grid."


@step(u'в гриде со столбцом "{column}" окна "{win_name}" '
      u'{condition:optional_in_}содержится подстрока "{test_row}"')
@step(u'в гриде на вкладке "{panel}" со столбцом "{column}" окна "{win_name}" '
      u'{condition:optional_in_}содержится подстрока "{test_row}"')
@step(u'в гриде с названием "{name}" окна "{win_name}" '
      u'{condition:optional_in_}содержится подстрока "{test_row}"')
def step_check_sub_row_in_grid(context, win_name, condition,
                               test_row, **kwargs):
    u"""
    Проверка наличия/отсутствия подстроки в гриде
    :param context: behave context
    :param win_name: Название окна.
    :param condition: Опциональная частица 'не' для проверки того, 
    что строки нет в гриде
    :param test_row: Проверяемая строка 
    :param kwargs: Вспомогательные параметры для локации грида.
    """
    win = get_win_object(context, win_name)
    if kwargs.get('panel') and kwargs.get('column'):
        grid = win.get_grid_by_parent_panel_and_column_header(
            kwargs.get('panel'), kwargs.get('column'))
    elif kwargs.get('name'):
        grid = win.get_grid_by_title(kwargs.get('name'))
    else:
        grid = win.get_grid_by_column_header(kwargs.get('column'))
    is_row_in_grid = [test_row in r['row'] for r in grid.get_rows()]
    if condition and condition == u'не':
        assert not any(is_row_in_grid), u"Row in grid."
    else:
        assert any(is_row_in_grid), u"Row not in grid."


@step(u'в гриде со столбцом "{column}" окна "{win_name}"'
      u' есть столбцы "{columns}"')
@step(u'в гриде со столбцом "{column}" на вкладке "{panel}" окна "{win_name}"'
      u' есть столбцы "{columns}"')
@step(u'в гриде с названием "{name}" окна "{win_name}"'
      u' есть столбцы "{columns}"')
def step_columns_in_grid(context, win_name, columns, **kwargs):
    u"""
    Проверка наличия столбцов в гриде.  
     :param context: behave context
    :param win_name: Название окна.
    :param columns: Список столбцов для проверки разделеных запятой. 
    :param kwargs: Вспомогательные параметры для локации грида.
    """
    win = get_win_object(context, win_name)
    if kwargs.get('panel') and kwargs.get('column'):
        grid = win.get_grid_by_parent_panel_and_column_header(
            kwargs.get('panel'), kwargs.get('column'))
    elif kwargs.get('name'):
        grid = win.get_grid_by_title(kwargs.get('name'))
    else:
        grid = win.get_grid_by_column_header(kwargs.get('column'))
    cols = columns.split(', ')
    assert all([c in list(grid.columns.keys()) for c in cols]), u"Cols not in grid"
