# -*- coding: utf-8 -*-
u"""
Набор степов для работы с полями формы (input type='text',
type='select', type='checkbox' и т.д.)
"""
from __future__ import absolute_import
from __future__ import unicode_literals

from datetime import datetime

import xlrd
from behave import step
from six.moves import range

from .winobject import DateField
from edutesting.ui_steps.winobject import Field
from .helpers import FIELDSET_NAMES
from .helpers import path_to_resource_file
from .helpers import waitForExtAjax
from .ui import get_win_object

# Возможные действия с чекбоксами и их булев эквивалент.
CHECK_ACTIONS = {
    u'включить': True,
    u'выключить': False,
}


# TODO: Вынести этот функционал в специальный класс Checkbox по аналогии с
#       классом DateField
def _click_box(box, action):
    u"""
    Включает/выключает чекбокс.

    Если чекбокс уже в необходимом состоянии, ничего не делает.

    :param box: объект чекбокс.
    :param action: включить/выключить.
    """
    assert action in CHECK_ACTIONS, (
        u'Такое нельзя делать с чекбоксом!'
    )
    if CHECK_ACTIONS[action] != box.is_checked():
        box.click()

# TODO тут убрать захардкоденный Enter, сделать принятие любых клавиш
@step(u'в поле {field_label} окна {win_name} установить значение {value}')
@step(u'в поле {field_label} окна {win_name} установить значение {value} и нажать {accept}')
def step_find_and_fill_field(context, field_label, win_name, value, accept=None):
    u"""
    Устанавливает значение value в поле field_label окна win_name.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    :param value: Данные которые необходимо установить в поле.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    if accept=='Enter':
        field.set_value_and_enter(value)
    else:
        field.set_value(value)


@step(u'в поле {field_label} окна {win_name} вставить "{value}" с помощью js')
def step_find_and_fill_field_with_js(context, field_label, win_name, value):
    u"""
    Устанавливает значение value в поле field_label окна win_name.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    :param value: Данные которые необходимо установить в поле.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.set_value_by_extjs(value)


@step(u'очистить поле {field_label} окна {win_name}')
def step_clear_field(context, field_label, win_name):
    u"""
    Удаляет данные из поля field_label.

    :param context: behave переменная, передается
     во все степы первым аргументом.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.clear()


@step(u'в поле {field_label} окна {win_name} нажать кнопку выпадающего'
      u' списка и выбрать значение {value}')
def step_find_and_fill_combobox(context, field_label, win_name, value):
    u"""
    Степ для выбора данных из выпадающего списка. В некоторых списках данные
    подгружаютсья ajax'ом, поэтому используется ожидание waitForExtAjax.

    :param context: behave переменная,
     передается во все степы первым аргументом.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    :param value: Данные которые необходимо выбрать в списке.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.click_by_trigger(u'выпадающего списка')

    waitForExtAjax(context)
    field.select_combobox_item(value)


@step(
    u'в поле {field_label} окна {win_name} ввести значение {value}'
    u' и из выпадающего списка выбрать {current_value}'
)
def step_enter_value_and_choose(
    context, field_label, win_name, value, current_value
):
    u"""
    Степ для выбора данных из поля с автокомплитом.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    :param value: Данные которые необходимо выбрать в списке.
    :param current_value: Текущее значение.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.set_value(value)

    context.webdriverwait.until(
        lambda d: d.execute_script(u"""
                var f = Ext.getCmp('{0}');
                var l = document.getElementById(f.list.id);
                return l.style['visibility'] == 'visible';
            """.format(field.field_id))
        )

    field.select_combobox_item(current_value)


@step(
    u'в поле {field_label} окна {win_name} нажать кнопку открытия '
    u'выбора из справочника'
)
def step_find_and_fill_combobox(context, field_label, win_name):
    u"""
    Степ для вызова справочника. При вызове справочника необходимо дождаться
    завершения ajax запросов, для этого используется waitForExtAjax.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.click_by_trigger(u'вызова справочника')
    waitForExtAjax(context)


@step(u'"{action}" чекбокс "{field_label}" окна "{win_name}"')
def step_click_checkbox_by_label(context, action, field_label, win_name):
    u"""
    Включение/Выключение чекбокса по подписи.

    :param context: behave-контекст степа.
    :param action: Действие над чекбоксом (включить/выключить).
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    """
    win = get_win_object(context, win_name)
    _click_box(win.get_field_by_name(field_label), action)


@step(u'{action} чекбокс {input_name}')
def step_click_checkbox_by_input_name(context, action, input_name):
    u"""
    Включение/Выключение чекбокса по названию <input> на форме.

    :param context: behave-контекст степа.
    :param action: Действие над чекбоксом (включить/выключить).
    :param input_name: Название поля на форме.
    """
    control = "//input[@name='%s']" % input_name
    web_element = context.browser.find_element_by_xpath(control)
    box = Field(web_element.get_attribute('id'), context.browser)
    _click_box(box, action)


@step(u'чекбокс {field_label} окна "{win_name}" {status}')
def step_checkbox_status_by_label(context, field_label, win_name, status):
    u"""
    Проверка состояния чекбокса, включен или выключен.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    :param status: Проверяемое состояние, включен или выключен
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    if status == u'включен':
        assert field.is_checked(), 'Checkbox is not checked'
    elif status == u'выключен':
        assert not field.is_checked(), 'Checkbox is not checked'


@step(u'в окне "{win_name}" есть поле "{field_label}"')
def step_(context, win_name, field_label):
    u"""
    Проверка есть ли поле field_label в окне win.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    """
    win = get_win_object(context, win_name)
    assert win.get_field_by_name(field_label), "Field doesn't exist."


@step(
    u'поле {field_label} окна {win_name} подсвечивается'
    u' {field_color} цветом'
)
def step_test_filed_valid(context, field_label, win_name, field_color):
    u"""
    Проверка каким цветом подсвечивается поле. Желтым подсвечивается
    обязательное, белым не обязательное.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    :param field_color: Цвет поля. может принимать значение (желтым, белым)
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    if field_color == u'желтым':
        assert not field.is_valid(), 'Field is not highlighted by yellow color'
    elif field_color == u'белым':
        assert field.is_valid(), 'Field is not highlighted by white color'


@step(u'в поле {field_label} окна {win_name} содержится значение {value}')
@step(u'в поле {field_label} окна {win_name} содержится значение "{value}"')
def step_test_value_in_field(context, field_label, win_name, value):
    u"""
    Степ для проверки содержится ли в поле value.

    Если необходимо проверить пустое ли поле тогда в качестве параметра value
    необходимо указать None.

    :param context: behave переменная,
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    :param value: Проверяемое значение.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    actual_value = [val.strip() for val in field.get_value().split(',')]
    if value == u'None' or value == ' ':
        value = ['']
    else:
        value = [val.strip() for val in value.split(',')]

    assert len(value) == len(actual_value), (
        "Count of records isn't equal"
    )
    for val in value:
        assert val in actual_value, 'Value not in field.'


@step(u'в поле {field_label} окна {win_name} содержится текущая дата')
@step(u'в поле {field_label} окна {win_name} занесется значение текущей даты')
def step_(context, field_label, win_name):
    u"""
    Степ для проверки содержится ли в поле текущая дата.

    :param context: behave переменная,
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    """
    context.execute_steps(
        u'Если в поле {0} окна {1} содержится значение {2}'.format(
            field_label, win_name, datetime.today().strftime('%d.%m.%Y')
        ))


@step(u'поле {field_label} окна {win_name} отображается с признаком '
      u'редактирования')
def step_is_field_edit(context, field_label, win_name):
    u"""
    Проверка редактировалось ли поле.

    При редактирование label поля становится фиолетовым.

    :param context: behave переменная,
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    assert field.is_edited()


# TODO: Отрефакторить этот степ так, чтобы избавиться от ворнингов.
@step(u'в выпадающем списке {field_label} окна {win_name} '
      u'будет запись {record}')
@step(u'в выпадающем списке {field_label} окна {win_name} '
      u'будет запись "{record}"')
@step(u'в выпадающем списке {field_label} значений из {is_fias}'
      u' окна {win_name} будет запись {record}')
@step(u'в выпадающем списке {field_label} окна {win_name}'
      u' совпадают значения с {country_file}')
def step_is_record_in_list(
    context,
    field_label,
    win_name,
    is_fias=None,
    record=None,
    country_file=None
):
    u"""
    Проверка того что в выпадающем списке содержится необходимое значение.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    :param record: Искомая запись.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    if record:
        if is_fias:
            if (u'Улица' in field_label) or (u'Дом' in field_label):
                is_exist = False
                for item in field.get_fias_list_items():
                    if record in item:
                        is_exist = True
                assert is_exist, 'Record not in list'
            else:
                assert record in field.get_fias_list_items(), (
                    'Record not in list')
        else:
            assert record in field.get_list_items(), 'Record not in list'
    else:
        country_list = field.get_list_items()
        wb = xlrd.open_workbook(
            path_to_resource_file(country_file,
                                  context.settings.PATH_TO_RES_DIR))
        sheet = wb.sheet_by_index(0)
        for rownum in range(1, sheet.nrows):
            assert sheet.row_values(rownum, 0)[0] in country_list, (
                'Record {} not in list'.format(sheet.row_values(rownum, 0)[0])
            )


@step(u'поле {field_label} окна "{win_name}" {status} для редактирования')
def step_is_field_editable(context, field_label, win_name, status):
    u"""
    Проверка доступно или не доступно для редактирование поле.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    :param status: Статус поля для проверки, доступно или недоступно.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    if status == u'недоступно':
        assert field.is_read_only(), 'Field is editable'
    elif status == u'доступно':
        assert not field.is_read_only(), 'Field is not editable'


@step(u'поле {field_name} блока {field_set} окна {win_name} неактивно')
def step_check_disabled_field(context, field_name, field_set, win_name):
    win = get_win_object(context, win_name)
    field_label = field_name + FIELDSET_NAMES[field_set]
    field = win.get_field_by_name(field_label)
    assert field.is_disabled()


@step(u'в поле {field_label} окна {win_name} прикрепить файл {file_name}')
def step_(context, field_label, win_name, file_name):
    u"""
    Прикрепление файла в поле типа file.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    :param file_name: Имя файла для добавления, файл должен храниться
     в папке features_selenium/steps/resources
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.attache_file(path_to_resource_file(
        file_name, context.settings.PATH_TO_RES_DIR)
    )


@step(u'в поле {field_label} окна {win_name} нажать кнопку {button}')
def step_press_field_button(context, field_label, win_name, button):
    u"""
    Нажатие кнопки у поля типа file.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    :param button: Название кнопка, может быть Загрузить,
      Очистить, Выбрать файл
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    if button == u'Загрузить':
        field.press_download_button()
    elif button == u'Очистить':
        field.press_clear_button()
    elif button == u'Выбрать файл':
        field.press_button_file()


@step(
    u'в окне {win_name} у поля "{field_label}"'
    u' {visible} кнопка {button_name}'
)
def step_is_file_button_visible(
    context, win_name, field_label, visible, button_name
):
    u"""
    Проверяет видимость кнопки загрузки и отчистки у поля для загрузки файлов.

    Входной параметр button_name должен быть либо Загрузить либо Очистить

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param visible: отображается/не отображается.
    :param win_name: Название окна в котором находится поле.
    :param button_name: Название кнопка, может быть Загрузить, Очистить.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    if visible == u'отображается':
        assert field.is_file_button_visible(button_name), (
            'Button is not visible.'
        )
    elif visible == u'не отображается':
        assert not field.is_file_button_visible(button_name), (
            'Button is visible'
        )


@step(
    u'у поля {field_label} окна "{win_name}"'
    u' {visible} кнопка {button}'
)
def step_is_field_button_visible(
    context, field_label, win_name, visible, button
):
    u"""
    Проверяет отображаются ли кнопки у поля.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    :param visible: отображается/не отображается
    :param button: Название кнопки, может быть очистить поле,
      выпадающего списка, вызова справочника.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    if visible == u'отображается':
        assert field.is_trigger_button_visible(button), (
            "Button is  not  visible."
        )
    elif visible == u'не отображается':
        assert not field.is_trigger_button_visible(button), (
            "Button is visible."
        )


@step(
    u'в окне {win_name} кликнуть по кнопке {trigger_name}'
    u' поля {field_label}'
)
def click_by_field_button(context, win_name, trigger_name, field_label):
    u"""
    Нажатие на кнопку поля (вызов справочника, вызов календаря и т.д.).

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    :param trigger_name: Название кнопки, может быть очистить поле,
      списка, вызова справочника.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.click_by_trigger(trigger_name)


@step(u'в поле {field_label} окна {win_name} вызвать календарь')
def step_open_data_picker(context, field_label, win_name):
    u"""
    Вызов виджета календаря у поля даты.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    """

    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.open_data_picker()


@step(u'у поля {field_label} окна {win_name} откроется виджет Календарь')
def step_is_date_widget_open(context, field_label, win_name):
    u"""
    Проверка открылся ли виджет календаря.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    assert field.is_data_picker_open(), "Data picker not opened"


@step(
    u'в виджете календаря поля {field_label} окна {win_name} отображается'
    u' текущая дата'
)
def step_widget_current_date(context, field_label, win_name):
    u"""
    Проверка отображается ли текущая дата в виджете календаря.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)

    # TODO: Необходимо сделать эту проверку более читаемой
    assert (field.widget_date_value().strftime('%d.%m.%Y') ==
            datetime.today().strftime('%d.%m.%Y')), (
        u"Values doesn't match. Expected {0} but found {1}".format(
            datetime.today().strftime('%d.%m.%Y'), field.get_value()
        )
    )


@step(
    u'в виджете Календаря поля {field_label} окна {win_name} '
    u'дата "{date}" {status} для выбора'
)
def step_is_widget_date_active(context, field_label, win_name, date, status):
    u"""
    Проверка доступна или нет дата date для выбора в виджете календаря.

    :param context: behave переменная.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    :param date: дата
    :param status: статус (доступна/не доступна)
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.open_data_picker()
    d = datetime.strptime(date, '%d.%m.%Y')
    if u'доступна' == status:
        assert d >= field.min_date() or d <= field.max_date(), (
            "Date is not active"
        )
    elif u'не доступна' == status:
        assert d <= field.min_date() or d >= field.max_date(), (
            "Date is active"
        )


@step(
    u'в поле {field_label} окна {win_name} нажать на кнопку '
    u'проставления текущей даты'
)
def step_set_current_date(context, field_label, win_name):
    u"""
    Нажатие кнопки выставления текущей даты у поля

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.set_current_date()


@step(
    u'в виджете Календаря поля {field_label} окна {win_name} '
    u'установить {date}'
)
def step_set_date_in_date_widget(context, field_label, win_name, date):
    u"""
    Выбор даты date в виджете календаря

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    :param date: Название окна в котором находится поле.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.set_date_in_widget(date)


@step(
    u'в окне {win_name} не отображается поле {field_name}'
    u' из блока {field_set}'
)
def step_check_field_is_invisible(context, win_name, field_name, field_set):
    win = get_win_object(context, win_name)
    field_label = field_name + FIELDSET_NAMES[field_set]
    field = win.get_field_by_name(field_label)
    assert not field.is_visible()


@step(u'у поля {field_label} окна {win_name} нажать кнопку очистить поле')
def step_clear_field(context, field_label, win_name):
    u"""
    Степ для очистки поля путем нажатия соотвествующей кнопки.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.click_by_trigger(u'очистить поле')


@step(
    u'кликнуть по полю с множественным выбором {field_label} окна'
    u' {win_name}'
)
def step_click_by_multi_select_field(context, field_label, win_name):
    u"""
    Степ осуществляющий клик по полю с мультиселектом для вызова
    выпадающего списка.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.field_object.click()


@step(
    u'в выпадающем списке поля {field_label} окна {win_name}'
    u' выбрать значение {value}'
)
def step_select_item(context, field_label, win_name, value):
    u"""
    Выбор значения из выпадающего списка.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    :param value: Значение которое будет вырабно
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.select_combobox_item(value)


@step(
    u'формат даты поля "{field_label}"'
    u' окна "{win_name}" соответствует "{date_format}"'
)
def step_date_field_format(context, field_label, win_name, date_format):
    u"""
    Проверка того что в поле дата проставляется в требуемом формате.

    :param context: behave-контекст степа.
    :param field_label: Название поля.
    :param win_name: Название окна в котором находится поле.
    :param date_format: Формат даты для проверки. Указывается в формате
    """
    d = datetime.now().strftime(date_format)
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.set_current_date()
    assert d == field.get_value(), u'Date formats not equal.'


@step(
    u'максимальное кол-во символов для ввода у поля "{field_label}"'
    u' окна "{win_name}" равно "{max_length}"'
)
def step_field_max_length(context, field_label, win_name, max_length):
    u"""
    Проверка наличия ограничение количества символов в поле.

    Проверяется есть ли у поля атрибут maxlength. Если нет то производиться
    попытка сохранить форму заполнив поле строкой длиннее max_length и
    проверить открылось ли окно с предупреждением
    о максимальном количестве символов.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    ml = field.field_object.get_attribute('maxlength')
    if ml:
        assert ml == max_length, u'Max length don\'t equal.'
    else:
        field.set_value('1' * (int(max_length) + 5))
        win.submit()
        alert_win = (get_win_object(context, u'Внимание') or
                     get_win_object(context, u'Проверка формы'))
        assert alert_win, u'Max length don\'t exists.'


@step(u'в поле "{field_label}" окна "{win_name}" запрещен ввод "{char_type}"')
def step_chars_limitation(context, field_label, win_name, char_type):
    u"""
    Проверка того что в поле запрещено вводить символы типа char_type.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    if char_type == u'букв':
        field.set_value('fortytwo')
    elif char_type == u'чисел':
        field.set_value(42)
    assert field.get_value() == '', (
        u'Input for {type} is enabled'.format(type=char_type)
    )


@step(u'тип поля "{field_label}" окна "{win_name}" является "{field_type}"')
def step_check_field_type(context, field_label, win_name, field_type):
    u"""
    Проверка что тип поля равен field_type.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    assert field.field_object.tag_name == field_type, u'Type don\'t match.'


@step(u'дважды кликнуть по полю "{field_label}" окна "{win_name}"')
def step_dblclick_by_field(context, field_label, win_name):
    u"""
    Двойной клик по полю
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    context.action.double_click(field.field_object).perform()


@step(
    u'в поле "{field_label}" окна "{win_name}" кол-во цифр после'
    u' запятой ограничено "{chars_amount:d}" знаками'
)
def step_limit_chars_after_comma(context, field_label, win_name, chars_amount):
    u"""
    Проверка того что кол-во цифр после запятой не больше chars_amount.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.set_value_and_enter(u','.join((u'42', u'0'*(chars_amount+1))))
    _, chars_after_comma = field.get_value().split(',')
    assert len(chars_after_comma) == chars_amount, (
        u'Chars amount is more than {}'.format(chars_amount)
    )


@step(
    u'в поле "{field_label}" окна "{win_name}"'
    u' можно ввести не более "{comma_amount:d}" запятой'
)
def step_comma_amount(context, field_label, win_name, comma_amount=1):
    u"""
    Проверка что в числовом поле можно ввести не больше comma_amount запятых.
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.set_value_and_enter(u'42,42' * (comma_amount + 1))
    val = field.get_value()
    assert val.count(',') == comma_amount, (
        u'In field more than {} commas'.format(comma_amount)
    )


@step(
    u'в поле "{field_label}" окна "{win_name}"'
    u' можно вводить дробные разделители в виде точки и запятой'
)
def step_number_delimeters(context, field_label, win_name):
    u"""
    Проверка универсальности дробного разделителя.

    (Можно вводить и запятую и точку).
    """
    win = get_win_object(context, win_name)
    field = win.get_field_by_name(field_label)
    field.set_value_and_enter(u'42,42')
    assert field.get_value() == u'42,42', u'Comma is restricted'
    field.set_value_and_enter(u'42.42')
    assert field.get_value() == u'42,42', u'Dot is restricted'
