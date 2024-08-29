# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import json
import time
import numbers

from datetime import datetime
from django.utils.html import strip_tags
from selenium.webdriver import Remote
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from .helpers import is_elem_exists
from .helpers import GENERIC_WAIT
from .helpers import WAIT_AJAX_BEGIN
import six


def get_displayed_web_element(driver, elem_id):
    u"""
    Получения элемента по его id и проверка того что у элемент статус
    отображения переведен в displayed.
    """
    wait = WebDriverWait(driver, GENERIC_WAIT)
    elem = driver.find_element_by_id(elem_id)
    try:
        wait.until(
            lambda d: elem.is_displayed()
        )
    except TimeoutException:
        return None
    else:
        return elem


def find_win_obj(context, win_obj):
    driver_wait = WebDriverWait(context.browser, GENERIC_WAIT)
    eval_el = context.browser.execute_script(
        'return window.GeneralEvalElement;'
    )

    if not eval_el or win_obj not in eval_el:
        try:
            win_obj = '' if win_obj == u'Nameless' else win_obj
            eval_el = driver_wait.until(
                lambda driver: driver.execute_script(
                    u"""return ui.find_popup_win('{}');""".format(win_obj)
                )
            )
        except TimeoutException:
            pass
    assert eval_el, u"Don't find window with title {0}".format(win_obj)

    if not isinstance(eval_el, dict):
        eval_el = json.loads(eval_el)

    eval_el = dict(
        (key.replace('&quot;', '"'), eval_el[key]) for key in eval_el
    )

    return eval_el


def get_win_object(context, win_name):
    u"""

    :param context: context: behave переменная для передачи данных между
    степами. Хранит словарь с открытыми extjs окнами.
    :param win_name: Имя окна
    :return: Объект класса Window
    :rtype: Window
    """
    win = None
    win_name = u'&#160;' if win_name == u'None' else win_name
    eval_el = find_win_obj(context, win_name)
    if win_name in eval_el:
        win_id = eval_el[win_name]['id']
        if (win_id in context.win_objects and
                win_name == context.win_objects[win_id].title):
            win = context.win_objects[eval_el[win_name]['id']]
        else:
            win = Window(eval_el[win_name]['id'], win_name, context.browser)
            context.win_objects[win.win_id] = win

    return win


class WinNotFound(Exception):
    pass


class FieldNotFound(KeyError):
    u"""
    Исключение возникает в случае если поле не найдено в окне.
    """
    pass


class GridNotFound(Exception):
    u"""
    Исключение возникает в случае если грид не найден в окне.
    """
    pass


class Desktop(object):
    u"""
    Класс для работы с элементами рабочего стола.

    :type driver: Remote
    :type icons: dict
    """

    def __init__(self, driver):
        self.driver = driver
        icons = self.driver.find_elements_by_xpath(
            "//table[@id='x-shortcuts']//td"
            "//div[@class='desktop-item-shortcut-label']")
        self.icons = {}
        for icon in icons:
            self.icons[icon.text] = icon

    def can_click_start_button(self, context):
        u"""
        Проверяет, можно ли кликнуть по кнопке "Пуск"
        :param context: behave-контекст степа.
        :return: bool
        """
        try:
            self.driver.find_element_by_id(self._get_start_id(context))
            return True
        except NoSuchElementException:
            return False

    def select_school(self):
        self.driver.execute_script('selectSchool();')

    def reset_school(self):
        self.driver.execute_script('resetSchool();')

    def select_period(self):
        self.driver.execute_script('selectPeriod();')

    def _get_start_id(self, context):
        u"""
        Возвращает идентификатор кнопки "Пуск".
        """
        if hasattr(context, 'start_id'):
            return context.start_id
        return self.driver.execute_script(
            'return AppDesktop.desktop.taskbar.startBtn.btnEl.id'
        )

    def __click_start_button(self, context):
        elem = self.driver.find_element_by_id(self._get_start_id(context))
        elem.click()

    def select_start_menu_item(self, elements, context):
        u"""
        ВЫбрать пункт в меню Пуск.

        Пуск -> Справочники -> Предметы
        Если пунктов меню нет, то будет ошибка KeyError
        """
        self.__click_start_button(context)
        parse_elements = [x.strip() for x in elements.split('->')]
        context.menu = {'items': json.loads(
            self.driver.execute_script("""
                console.log("No way!", ui);
                recursemenuItem = ui.recursemenuItem;
                items = recursemenuItem(AppDesktop.launcher.items);
                toolItems = recursemenuItem(
                    AppDesktop.launcher.toolItems
                );

                for (var key in toolItems){
                    items[key] = toolItems[key]
                };

                return Ext.util.JSON.encode(items);
            """)
        )}
        item = context.menu

        for i in parse_elements:
            item = item['items'][i]
            elem = context.webdriverwait.until(
                lambda d: get_displayed_web_element(d, item['id'])
            )
            # При повторном открытие меню пуск webdriver не может найти
            #  элементы списка, поэтому здесь повторная попытка найти элемент
            try:
                elem.click()
            except ElementNotVisibleException:
                elem = context.webdriverwait.until(
                    lambda d: get_displayed_web_element(d, item['id'])
                )
                elem.click()

    def click_by_icon(self, icon_name):
        u"""
        Клик по иконке рабочего стола.
        """
        if icon_name in self.icons:
            self.icons[icon_name].click()

    def is_icon_exists(self, icon_name):
        u"""
        Проверка сущ. иконки на на рабочем столе

        :rtype bool
        """
        if icon_name in self.icons:
            return True
        else:
            return False


class Window(object):
    u"""
    Класс для работы с extjs window.

    Реализует методы работы с окном и доступа к элементам окна
    (поля, кнопки, гриды и т.д.).

    :type driver: Remote
    :type win_obj: WebElement
    """

    text = ''

    def __init__(self, win_id, title, driver):
        assert isinstance(driver, Remote)
        self.win_id = win_id
        self.title = title
        self.driver = driver
        self.webdriverwait = WebDriverWait(self.driver, 40)
        self.win_obj = self.driver.find_element_by_id(win_id)
        # Словарь вида {field_label: field_id}
        self.fields_init_data = {}
        # Словарь вида {field_label: FieldObj}
        self.init_fields = {}
        self.grids = {}
        self.button_init_data = {}
        self.init_buttons = {}
        self.htmleditors = {}
        self.__init_win_fields()
        self.__init_win_buttons()

    def __init_win_fields(self):
        u"""
        Метод инициализирует данные о текстовых полях (input type='text').

        В словарь fields_init_data сохраняется id поля и флаг указывающий
        является ли поле Date, ключем является название поля (label).
        В данном методе не создается объект Field т.к. у окна может быть
        несколько вкладок и если поле находится на еще не открытой вкладке
        то оно не доступно для webdriver.
        """
        self.fields_init_data = {}
        labels = self.driver.execute_script(u"""
            return win_helpers.get_win_labels('{0}')
        """.format(self.win_id))
        for f in labels:
            if f['label'] not in self.fields_init_data:
                self.fields_init_data[f['label']] = {
                    'id': f['id'],
                    'is_date': f['is_date']
                }
            else:
                count = 0
                for fid in self.fields_init_data:
                    if f['label'] in fid:
                        count += 1
                f['label'] += '-' + str(count)
                self.fields_init_data[f['label']] = {
                    'id': f['id'],
                    'is_date': f['is_date']
                }

    def __init_win_grids(self):
        self.grids = {k: v for k, v in six.iteritems(self.grids)
                      if is_elem_exists(self.driver, v.grid_id)}
        grids = self.driver.find_elements_by_xpath(
            u"//div[@id='{0}']"
            u"//div[contains(@class, 'x-grid-panel')]".format(self.win_id)
        )
        for g in grids:
            if (g.get_attribute('id') not in self.grids and
                    'comp' not in g.get_attribute('id')):
                have_columns_groups = self.driver.execute_script(u"""
                    return (Ext.getCmp('{id}').colModel.hasOwnProperty('rows')
                            && Ext.getCmp('{id}').colModel.rows.length !== 0);
                """.format(id=g.get_attribute('id')))
                if have_columns_groups:
                    grid = GridWithGroupColumns(
                        g.get_attribute('id'),
                        self.driver
                    )
                else:
                    grid = Grid(g.get_attribute('id'), self.driver)
                self.grids[grid.grid_id] = grid

    def __init_field(self, field_label):
        self.__init_win_fields()
        try:
            if self.fields_init_data[field_label]['is_date']:
                field = DateField(
                    self.fields_init_data[field_label]['id'],
                    self.driver,
                    field_label)
            else:
                field = Field(
                    self.fields_init_data[field_label]['id'],
                    self.driver,
                    field_label)
            self.init_fields[field_label] = field
        except KeyError:
            raise FieldNotFound(
                u'Поле "{0}" в окне "{1}" не найдено.'.format(
                    field_label, self.title))

    def __init_win_buttons(self):
        self.button_init_data = self.driver.execute_script(u"""
            return win_helpers.get_win_buttons('{0}')
        """.format(self.win_id))

    def submit(self):
        self.driver.execute_script(u"""
            w = Ext.getCmp('{win_id}');
            if (w.submitForm !== undefined) {{
                w.submitForm();
            }}
        """.format(win_id=self.win_id))

    def is_open(self):
        return self.driver.execute_script(u"""
            return win_helpers.is_open('{0}')
        """.format(self.win_id))

    def is_close(self):
        return self.webdriverwait.until(
            lambda driver: driver.execute_script(u"""
                return win_helpers.is_close('{0}');
            """.format(self.win_id))
        )

    def close(self):
        self.driver.execute_script(u"""
            Ext.getCmp('{0}').close()
        """.format(self.win_id))

    def get_button_by_name(self, button_name):
        if button_name in self.init_buttons:
            return self.init_buttons[button_name]
        else:
            if button_name in self.button_init_data:
                button = Button(button_name,
                                self.button_init_data[button_name],
                                self.driver)
                self.init_buttons[button_name] = button
                return button
            else:
                return None

    def get_atr_btn(self, btn):
        id_el = self.button_init_data[btn]
        return id_el

    def get_field_by_name(self, field_label):
        u"""
        Возвращает объект типа Field по его названию

        :rtype Field
        """
        if field_label in self.init_fields:
            return self.init_fields[field_label]
        else:
            self.__init_field(field_label)
            return self.init_fields[field_label]

    def get_fieldset_by_name(self, fieldset_name):
        u"""
        Возвращает объект типа Fieldset по его названию

        :rtype Fieldset
        """
        fieldset_list = self.driver.find_elements_by_xpath(
            "//div[@id='{0}']//fieldset".format(self.win_id)
        )
        fieldset = None
        for fs in fieldset_list:
            try:
                span = fs.find_element_by_tag_name('span')
            except NoSuchElementException:
                continue
            if span.text == fieldset_name:
                fieldset = Fieldset(
                    fieldset_name,
                    fs.get_attribute('id'),
                    self.driver
                )
                break
        return fieldset

    def get_grid_by_column_header(self, column_header):
        u"""
        Поиск грида по заголовку столбца

        :rtype Grid
        """
        self.__init_win_grids()
        for gid, gobj in six.iteritems(self.grids):
            if column_header in gobj.columns:
                return gobj
        else:
            raise GridNotFound(
                u'Грид со столбцом "{0}" в окне "{1}" не найден'.format(
                    column_header, self.title
                ))

    def get_grid_by_column_list(self, columns_list):
        u"""
        Поиск грида по списку всех его столбцов, полезно если на в одном окне
        на одной панели есть гриды с одинаковым столбцом(-ами).
        column_list строка содержащая список столбцов через запятую

        :rtype Grid
        """
        columns_list = columns_list.replace(', ', ',').split(',')
        self.__init_win_grids()
        for gid, gobj in six.iteritems(self.grids):
            if set(columns_list) == set(gobj.columns):
                return gobj
        else:
            raise GridNotFound(
                u'Грид со столбцами "{0}" в окне "{1}" не найден'.format(
                    columns_list, self.title
                ))

    def get_grid_by_parent_panel_and_column_header(self, panel_name,
                                                   column_header):
        u"""
        Поиск грида на определенной панели по заголовку столбца

        :rtype Grid
        """
        self.__init_win_grids()
        grids = []
        for gid, gobj in six.iteritems(self.grids):
            if panel_name == gobj.get_grid_parent_panel():
                grids.append(gobj)
        for g in grids:
            if column_header in g.columns:
                return g
        else:
            raise GridNotFound(
                u'Грид со столбцом "{0}" в окне "{1}" на вкладке {2}'
                u' не найден'.format(
                    column_header, self.title, panel_name
                ))

    def get_grid_by_button_name(self, button_name):
        u"""
        Поиск грида по названию кнопки на панели грида.

        :rtype Grid
        """
        self.__init_win_grids()
        for gid, gobj in six.iteritems(self.grids):
            if button_name in gobj.grid_panels['control'].buttons:
                return gobj
        else:
            raise GridNotFound(
                u'Грид со кнопкой "{0}" в окне "{1}" не найден'.format(
                    button_name, self.title
                ))

    def get_grid_by_title(self, grid_title):
        u"""
        Получение объекта типа Grid по его заголовку
        :param grid_title: Заголовок грида
        :return: Объект типа Grid в случае если сущ. грид с таким заголовком,
        иначе будет вызвано исключение GridNotFound
        :rtype Grid
        """
        self.__init_win_grids()
        for gid, gobj in six.iteritems(self.grids):
            if gobj.title == grid_title:
                return gobj
        else:
            raise GridNotFound(u'Грид с заголовком "{0}" не найден'.format(
                grid_title))

    def get_tab_by_name(self, tab_name):
        return self.driver.execute_script(u"""
            return win_helpers.get_tab_by_name('{0}', '{1}')
        """.format(self.win_id, tab_name))

    def open_tab(self, tab_name):
        return self.driver.execute_script(u"""
            Ext.getCmp('{0}').show()
        """.format(self.get_tab_by_name(tab_name)))

    def is_tab_open(self, tab_name):
        return self.driver.execute_script(u"""
            return win_helpers.is_tab_visible('{0}', '{1}')
        """.format(self.win_id, tab_name))

    def is_tab_active(self, tab_name):
        return self.driver.execute_script(u"""
            return win_helpers.is_tab_active('{0}', '{1}')
        """.format(self.win_id, tab_name))

    def get_htmleditor(self, htmleditor_name):
        u"""
        :param htmleditor_name: это значение атрибута name у textarea
         html редактора
        :return: Объект HtmlEditor
        :rtype HtmlEditor
        """
        if htmleditor_name in self.htmleditors:
            return self.htmleditors[htmleditor_name]
        else:
            htmleditors = self.driver.execute_script(u"""
                return win_helpers.get_win_htmleditors('{0}')
            """.format(self.win_id))
            for h in htmleditors:
                if htmleditor_name in h:
                    editor = HtmlEditor(htmleditor_name,
                                        htmleditors[htmleditor_name],
                                        self.driver)
                    self.htmleditors[htmleditor_name] = \
                        editor
                    return editor

    def get_text(self):
        u"""
        :return: Возвращает текст находящийся на окне
        """
        if not self.text:
            text = self.driver.execute_script(u"""
                return win_helpers.get_text('{0}')
            """.format(self.win_id))
            self.text = text if text else self.win_obj.text
        return self.text


class Field(object):
    u"""
    Класс для работы с extjs field

    :type driver: Remote
    :type field_object: WebElement
    :type wait: WebDriverWait
    """

    def __init__(self, field_id, driver, field_label=None):
        self.field_id = field_id
        self.label = field_label
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 25)

        self.field_object = get_displayed_web_element(driver, self.field_id)

    def __wait_ajax_combo_list(self):
        u"""
        Ожидание появления выпадающего списка загружаемого ajax'ом.
        """
        list_id = self.driver.execute_script(u"""
                var f = Ext.getCmp('{0}');
                return f.list.dom.id;
            """.format(self.field_id)
        )
        self.wait.until(
            lambda d: d.find_elements_by_xpath(
                "//div[@id='{0}' and contains(@style, 'visibility: visible')]"
                "//div[contains(@class, 'x-combo-list-item')]".format(list_id)
            )
        )

    def get_value(self):
        return (self.driver.execute_script(u"""
            return field_helper.get_value('{0}')
        """.format(self.field_id))).rstrip()

    def set_value(self, value):
        self.field_object.click()
        self.field_object.clear()
        self.field_object.send_keys(value)

    def set_value_by_extjs(self, value):
        return self.driver.execute_script(u"""
            Ext.getCmp('{0}').setValue('{1}')
        """.format(self.field_id, value))

    # TODO по хорошему сделать более универсальную функцию со словарем клавиш
    def set_value_and_enter(self, value):
        u"""
        Задать значение и после нажать Enter
        """
        self.set_value(value)
        self.field_object.send_keys(Keys.ENTER)

    def clear(self):
        self.field_object.clear()

    def is_valid(self):
        return self.driver.execute_script(u"""
            return field_helper.is_valid('{0}')
        """.format(self.field_id))

    def is_visible(self):
        if self.field_object:
            return self.driver.execute_script(u"""
                return field_helper.is_visible('{0}')
            """.format(self.field_id))
        else:
            return False

    def is_edited(self):
        return self.driver.execute_script(u"""
            return field_helper.is_edited('{0}')
        """.format(self.field_id))

    def is_checked(self):
        return self.field_object.get_attribute('checked')

    def is_read_only(self):
        return bool(self.field_object.get_attribute('readonly') or
                    self.field_object.get_attribute('disabled'))

    def is_disabled(self):
        return bool(self.field_object.get_attribute('disabled'))

    def attache_file(self, file_path):
        upload_field_name = self.driver.execute_script(u"""
            return field_helper.get_upload_field_name('{0}')
        """.format(self.field_id))
        if upload_field_name:
            upload_field = self.driver.find_element_by_name(upload_field_name)
            upload_field.send_keys(file_path)

    def is_file_button_visible(self, button_name):
        u"""
        Проверяет, отображаются ли кнопки загрузки и отчистки
        у поля для загрузки файлов. Входной параметр button_name должен быть
        либо, Загрузить либо, Очистить.
        """
        button_class = None
        if button_name == u'Загрузить':
            button_class = u'download'
        elif button_name == u'Очистить':
            button_class = u'clear'
        parent_id = self.driver.find_element_by_xpath(
            u"//label[@for='{label_id}']"
            u"/parent::div".format(label_id=self.field_id)
        ).get_attribute('id')
        return self.driver.find_element_by_xpath(
            u"//div[@id='{pid}']"
            u"//button[contains(@class, "
            u"'x-form-file-{button_class}-icon')]".format(
                pid=parent_id, button_class=button_class
            )
        ).is_displayed()

    def is_trigger_button_visible(self, trigger_name):
        return bool(self.get_trigger_by_type(trigger_name))

    def get_trigger_by_type(self, trigger_name):
        u"""
        :param trigger_name: Название триггера из словаря triggers.
        :return: html id триггера
        """
        triggers = {
            u'очистить поле': 0,
            u'выпадающего списка': 1,
            u'вызова справочника': 2,
        }
        return self.driver.execute_script(u"""
            return field_helper.get_trigger_by_type('{0}', '{1}')
        """.format(self.field_id, triggers[trigger_name]))

    def click_by_trigger(self, trigger_name):
        trigger_id = self.get_trigger_by_type(trigger_name)
        expanded = self.driver.execute_script(
            u'return Ext.getCmp("{}").isExpanded();'.format(self.field_id)
        )
        if not expanded:
            (self.driver.find_element_by_id(trigger_id)).click()

    def get_list_items(self):
        u"""
        Возвращает словарь вида {list_item_id:list_item_value} c содержимым
         выпадающего списка. Предварительно дожидается открытие списка.
        """
        self.wait.until(
            lambda d: d.execute_script(u"""
                var f = Ext.getCmp('{0}');
                var l = document.getElementById(f.list.id);
                return l.style['visibility'] == 'visible';
            """.format(self.field_id))
        )
        list_items = self.wait.until(
            lambda driver: driver.execute_script(u"""
                return field_helper.get_list_items('{0}')
            """.format(self.field_id))
        )
        return list_items

    def get_fias_list_items(self):
        u"""
        Возвращает словарь вида {list_item_id:list_item_value} c содержимым
        выпадающего списка, где значения грузятся из ФИАС.
        Предварительно дожидается открытие списка.
        """
        self.__wait_ajax_combo_list()
        return self.driver.execute_script(u"""
            return field_helper.get_fias_list_items('{0}', '{1}')
        """.format(self.field_id, self.label))

    def press_download_button(self):
        self.driver.execute_script(u"""
            return field_helper.press_field_button('{0}', "buttonDownload")
        """.format(self.field_id))

    def press_clear_button(self):
        self.driver.execute_script(u"""
            return field_helper.press_field_button('{0}', "buttonClear")
        """.format(self.field_id))

    def press_button_file(self):
        self.driver.execute_script(u"""
            return field_helper.press_field_button('{0}', "buttonFile")
        """.format(self.field_id))

    def click(self):
        self.field_object.click()

    def select_combobox_item(self, value):
        self.__wait_ajax_combo_list()
        combo_id = self.driver.execute_script(u"""
            return Ext.getCmp('{0}').innerList.dom.id;
        """.format(self.field_id))
        items = self.driver.find_elements_by_xpath(
            "//div[@id='{0}']/div".format(combo_id)
        )
        search_item = None
        for item in items:
            if item.text.strip() == value.strip():
                search_item = item
                break
        assert search_item, u'Not found value %s in %s' % (value, self.label)
        search_item.click()


class DateField(Field):
    u"""
    Класс для работы с полями типа m3-date.
    """

    def open_data_picker(self):
        self.driver.find_element_by_xpath(u"""
            //input[@id='{f_id}']
            /..//img[contains(@class, 'x-form-date-trigger')]
        """.format(f_id=self.field_id)).click()

    def is_data_picker_open(self):
        return self.driver.execute_script(u"""
            return Ext.getCmp('{0}').menu.picker.isVisible();
        """.format(self.field_id))

    def min_date(self):
        str_date = self.driver.execute_script(u"""
            return field_helper.date_picker_min_date('{0}')
        """.format(self.field_id))
        return datetime.strptime(str_date, '%d.%m.%Y')

    def max_date(self):
        str_date = self.driver.execute_script(u"""
            return field_helper.date_picker_max_date('{0}')
        """.format(self.field_id))
        return datetime.strptime(str_date, '%d.%m.%Y')

    def set_current_date(self):
        self.driver.find_element_by_xpath(u"""
            //input[@id='{f_id}']
            /..//img[contains(@class, 'x-form-current-date-trigger')]
        """.format(f_id=self.field_id)).click()

    def get_value(self):
        return self.driver.execute_script(u"""
            return field_helper.get_value('{0}');
        """.format(self.field_id))

    def set_date_in_widget(self, str_date):
        u"""
        :param str_date: Дата для установки в виджете.
         Должна быть в формате d.m.Y.
        """
        date = datetime.strptime(str_date, '%d.%m.%Y')
        self.driver.execute_script(u"""
            return field_helper.set_date_in_widget(
                '{f_id}', {y}, {m}, {d}
            );
        """.format(f_id=self.field_id, y=date.year, m=date.month, d=date.day))

    def widget_date_value(self):
        str_date = self.driver.execute_script(u"""
            return field_helper.get_date_picker_value('{0}');
        """.format(self.field_id))
        return datetime.strptime(str_date, '%d.%m.%Y')

    def is_trigger_button_visible(self, button_name):
        date_picker = None
        if button_name == u'Календарь':
            date_picker = u"""
                //input[@id='{f_id}']/..//
                img[contains(@class, 'x-form-trigger')
                and contains(@class, 'x-form-date-trigger')]
            """.format(f_id=self.field_id)
        elif button_name == u'Текущая дата':
            date_picker = u"""
                //input[@id='{f_id}']/..//
                img[contains(@class, 'x-form-trigger')
                and contains(@class, 'x-form-current-date-trigger')]
            """.format(f_id=self.field_id)
        return bool(self.driver.find_elements_by_xpath(date_picker))


class Grid(object):
    u"""
    Класс для работы с grid

    :type driver: Remote
    :type grid_object: WebElement
    """

    def __init__(self, grid_id, driver):
        self.grid_id = grid_id
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.grid_object = driver.find_element_by_id(grid_id)
        self.columns = self.__get_grid_columns()
        self.grid_panels = {}
        self.__get_grid_panels()
        self.title = self.driver.execute_script(u"""
            return Ext.getCmp('{grid_id}').title
        """.format(grid_id=self.grid_id)) or u''

    def __get_grid_columns(self):
        u"""
        Возвращает словарь где ключом будет заголовок столбца
        а значением словарь содержащий id столбца и значение dataIndex
        """
        return self.driver.execute_script(u"""
            return grid_helper.get_grid_columns('{0}')
        """.format(self.grid_id))

    def __get_grid_panels(self):
        panels = self.driver.execute_script(u"""
            return grid_helper.get_grid_panels('{0}')
        """.format(self.grid_id))
        if panels:
            for p in panels:
                panel = GridPanel(panels[p], self.driver)
                self.grid_panels[p] = panel

    def click_by_row(self, value):
        path_to_rows = """
            //div[@id='{grid_id}']//div[contains(@class, 'x-grid3-row')]
        """.format(grid_id=self.grid_id)
        rows = self.driver.find_elements_by_xpath(path_to_rows)
        v = None
        for r in rows:
            if value in r.text:
                v = r
                break
        assert v, u'Not found value %s' % value
        v.click()

    def select_row_by_column_value(self, column, value):
        u"""
        Данный метод выберет запись в гриде, при этом сохранить выделение уже
        выбранных записей.
        """
        row = self.get_row_by_column_value(column, value)
        assert row, u"Row is not exists"
        self.driver.execute_script(u"""
            grid_helper.select_row_by_column_value('{0}', '{1}')
        """.format(self.grid_id, row['id']))

    def select_all_rows(self):
        self.driver.execute_script(u"""
            grid_helper.select_all_rows('{0}')
        """.format(self.grid_id))

    def clear_selection(self, column=None, row_value=None):
        row_id = ''
        if column and row_value:
            idx = self.columns[column]['dataIndex']
            row_id = [r['id'] for r in self.get_rows()
                      if r[idx] == row_value].pop()
        self.driver.execute_script(u"""
            grid_helper.clear_selection('{0}', '{1}')
        """.format(self.grid_id, row_id))

    def is_all_rows_selected(self):
        rows = self.driver.execute_script(u"""
            return grid_helper.get_selected_rows('{0}', '')
        """.format(self.grid_id))
        return len(rows) == len(self.get_rows())

    def is_row_selected(self, column, row_value):
        row_id = self.get_row_by_column_value(column, row_value)['id']
        return bool(self.driver.execute_script(u"""
            return grid_helper.get_selected_rows('{0}', '{1}')
        """.format(self.grid_id, row_id)))

    def get_rows(self):
        u"""
        Возвращает словарь содержащий id строки, и содержимое строки
        по столбцам
        """
        return self.driver.execute_script(u"""
            return grid_helper.get_rows('{0}')
        """.format(self.grid_id))

    def get_total_rows_len(self):
        return self.driver.execute_script(u"""
            return grid_helper.get_total_rows_len('{0}')
        """.format(self.grid_id))

    def get_selected_rows(self):
        return self.driver.execute_script(u"""
            return grid_helper.get_selected_rows('{0}')
        """.format(self.grid_id))

    def get_grid_parent_panel(self):
        return self.driver.execute_script(u"""
            return grid_helper.get_grid_parent_panel('{0}')
        """.format(self.grid_id))

    def click_by_row_value(self, column, value):
        self.select_row_by_column_value(column, value)
        xpath_to_grid_cell = """
            //div[contains(@class, 'x-grid3-row-selected')]
            //div[contains(@class, 'x-grid3-col-{col_id}')]
            /child::node()""".format(col_id=self.columns[column]['id'])
        cell = self.wait.until(
            lambda d: d.find_element_by_xpath(xpath_to_grid_cell)
        )
        cell.click()

    def click_by_selected_cell(self, column_name=None):
        try:
            xpath_to_grid_cell = """
            //td[contains(@class, 'x-grid3-cell-selected')]"""
            cell = self.driver.find_element_by_xpath(xpath_to_grid_cell)
        except NoSuchElementException:
            col_dict = self.columns
            xpath_to_grid_cell = """
                //div[contains(@class, 'x-grid3-col-{0}')]
            """.format(col_dict[column_name]['id'])
            cell = self.driver.find_element_by_xpath(xpath_to_grid_cell)

        ActionChains(self.driver).double_click(cell).perform()

    def get_editor_id(self, column_name):
        for column in self.columns.keys():
            if column == column_name:
                return self.columns[column]['editorId']

    def select_cell_by_row_value(self, target_column, row_value, row_column):
        row_idx = self.get_row_by_column_value(row_column, row_value)['id']
        col_data_index = self.columns[target_column]['dataIndex']
        if row_idx:
            self.driver.execute_script(u"""
                grid_helper.select_cell_by_column('{0}', '{1}', '{2}', '{3}')
            """.format(self.grid_id, row_idx, col_data_index, target_column))
        else:
            help_col_idx = self.columns[row_column]['dataIndex']
            self.driver.execute_script(u"""
                grid_helper.select_cell_by_row_value('{0}', '{1}',
                                                      '{2}', '{3}')
            """.format(self.grid_id, row_value, col_data_index, help_col_idx))

    def set_value_in_active_cell(self, column, value):
        cell = self.grid_object.find_element_by_id(
            self.columns[column]['editorId']
        )
        cell.clear()
        cell.send_keys(value)
        cell.send_keys(Keys.ENTER)

    def set_value_in_cell(self, column, value, help_column, help_column_val):
        row_id = self.get_row_by_column_value(
            help_column,
            help_column_val
        )['id']
        if row_id:
            self.driver.execute_script(u"""
                return grid_helper.set_value_in_cell(
                    '{0}', '{1}', '{2}', '{3}'
                )
            """.format(
                self.grid_id, row_id, self.columns[column]['dataIndex'], value
            ))

    def get_cell_value(self, target_column, row_value, help_column):
        row = self.get_row_by_column_value(help_column, row_value)
        if row:
            return row[self.columns[target_column]['dataIndex']]

    def get_row_by_column_value(self, column, value):
        assert column in self.columns, "Column doesn't exist"
        idx = self.columns[column]['dataIndex']
        for r in self.get_rows():
            if isinstance(r[idx], numbers.Number):
                r[idx] = str(r[idx])
            if value == strip_tags(r[idx]):
                return r
            # TODO Вынести в отдельный метод.
            elif value in strip_tags(r[idx]):
                return r

    def next_page(self):
        panel_id = self.grid_panels['paginator'].panel_id
        self.driver.execute_script(u"""
            return grid_panel_helper.scroll_page('{0}', 'next')
        """.format(panel_id))

    def prev_page(self):
        panel_id = self.grid_panels['paginator'].panel_id
        self.driver.execute_script(u"""
            return grid_panel_helper.scroll_page('{0}', 'prev')
        """.format(panel_id))

    def is_enabled(self):
        return not self.driver.execute_script(u"""
            return Ext.getCmp('{0}').disabled
        """.format(self.grid_id))

    def get_column_data_index(self, column):
        return self.columns[column]['dataIndex']

    def get_column_list_items(self, column):
        if column in self.columns and 'editorId' in self.columns[column]:
            return self.driver.execute_script(u"""
                return field_helper.get_list_items('{0}')
            """.format(self.columns[column]['editorId']))
        else:
            return None

    def select_combobox_item(self, column, value):
        combo_id = self.driver.execute_script(u"""
            return Ext.getCmp('{0}').innerList.dom.id;
        """.format(self.columns[column]['editorId']))
        items = self.driver.find_elements_by_xpath(
            "//div[@id='{0}']/div".format(combo_id)
        )
        search_item = None
        for item in items:
            if item.text.strip() == value.strip():
                search_item = item
                break
        assert search_item, u'Not found value %s in %s' % (value, column)
        search_item.click()


class GridWithGroupColumns(Grid):
    u"""
    Класс для работы с гридоми в которых есть группировка по столбцами

    Пример грида:
    -----------------------------------------------------------
    |       |       |  group1     |    group2   |  group3     |
    |       |       |-------------|-------------|-------------|
    |  col1 |  col2 | col3 | col4 | col5 | col6 | col7 | col8 |
    |-------|-------|------|------|------|------|------|------|
    |       |       |      |      |      |      |      |      |
    -----------------------------------------------------------

    Метод grid.__get_grid_columns() для приведенного грида сформирует словарь с
    ключами след. вида:
        grid.colums = {
            col1: column_data,
            col2: column_data,
            col3-group1: column_data,
            col4-group1: column_data,
            col5-group2: column_data,
            col6-group2: column_data,
            col7-group3: column_data,
            col8-group3: column_data,
        }

    """

    def __init__(self, grid_id, driver):
        super(GridWithGroupColumns, self).__init__(grid_id, driver)
        self.columns = self.__get_grid_columns()

    def __get_grid_columns(self):
        return self.driver.execute_script(u"""
            return grid_helper.get_grid_group_columns('{0}')
        """.format(self.grid_id))

    def set_value_in_cell(self, full_col_name, value,
                          help_column, help_column_val):
        u"""
        Устанавливает value в ячейку грида.

        :param value: Значение для заполнения ячейки,
        :param full_col_name: Полное название столбца. Если есть группировка то
        формируется след. образом col_name + '-' + group_name
        :param help_column: Вспомогательный столбец для локации строки.
        :param help_column_val: Значение в вспомогательном столбце.
        """
        row = self.get_row_by_column_value(help_column, help_column_val)
        row_id = row.get('index') or row.get('id')
        if not row_id:
            row_id = row.get('total_hours')
        if row_id:
            self.driver.execute_script(u"""
                return grid_helper.set_value_in_cell(
                    '{0}', '{1}', '{2}', '{3}', '{4}'
                )
            """.format(
                self.grid_id,
                row_id,
                self.columns[full_col_name]['dataIndex'],
                value,
                self.columns[help_column]['dataIndex']
            ))

    def get_cell_value(self, full_col_name, help_column_val, help_column):
        u"""
        Получение значения из ячейки

        :param full_col_name: Полное название столбца. Если есть группировка то
        формируется след. образом col_name + '-' + group_name
        :param help_column: Вспомогательный столбец для локации строки.
        :param help_column_val: Значение в вспомогательном столбце.
        """
        row = self.get_row_by_column_value(help_column, help_column_val)
        if row:
            data = row[self.columns[full_col_name]['dataIndex']]
            if isinstance(data, six.string_types):
                data = strip_tags(data.replace('\n', ' '))
            elif isinstance(data, list):
                data = data[0]
                try:
                    data = strip_tags(
                        data['display'].replace('\n', ' ')
                    ).strip()
                except KeyError:
                    data = None
            return data


class GridPanel(object):
    u"""
    Класс для работы с grid panel и кнопками расположенными на панели.

    :type driver: Remote
    """

    def __init__(self, panel_id, driver):
        self.panel_id = panel_id
        self.driver = driver
        self.buttons = self.__get_buttons()

    def __get_buttons(self):
        return self.driver.execute_script(u"""
            return grid_panel_helper.get_buttons('{0}')
        """.format(self.panel_id))

    def press_button(self, button_name):
        button = self.driver.find_element_by_id(self.buttons[button_name])
        button.click()

    def is_button_exist(self, button_name):
        return button_name in self.buttons

    def is_button_enabled(self, button_name):
        return not self.driver.execute_script(u"""
            return Ext.getCmp('{0}').disabled
        """.format(self.buttons[button_name]))

    def is_enabled(self):
        return not self.driver.execute_script(u"""
            return Ext.getCmp('{0}').disabled
        """.format(self.panel_id))


class Button(object):
    u"""
    Класс для работы с кнопками расположенными на окне, за исключением кнопок
    из grid panel.

    :type driver: Remote
    """

    def __init__(self, button_name, button_id, driver):
        self.name = button_name
        self.button_id = button_id
        self.driver = driver

    def click(self):
        (self.driver.find_element_by_id(self.button_id)).click()
        time.sleep(WAIT_AJAX_BEGIN)  # Ожидаем возможный запуск ajax запроса.

    def is_enabled(self):
        return not self.driver.execute_script(u"""
            return Ext.getCmp('{0}').disabled
        """.format(self.button_id))


class HtmlEditor(object):

    def __init__(self, htmleditor_name, htmldeditor_id, driver):
        self.name = htmleditor_name
        self.editor_id = htmldeditor_id
        self.driver = driver
        self.editor_obj = self.driver.find_element_by_id(htmldeditor_id)

    def set_value(self, value):
        u"""
        Установить значение через send_keys не получается т.к. textarea
         подменяется фреймом, поэтому через js.
        """
        self.driver.execute_script(u"""
            Ext.getCmp('{0}').setValue('{1}')
        """.format(self.editor_id, value))

    def get_value(self):
        return self.driver.execute_script(u"""
            return Ext.getCmp('{0}').getValue()
        """.format(self.editor_id))


class Fieldset(object):
    u"""
    Класс для работы с элементами управления блоков с полями
    """
    def __init__(self, fieldset_name, fieldset_id, driver):
        self.name = fieldset_name
        self.id = fieldset_id
        self.driver = driver
        self.fieldset_obj = self.driver.find_element_by_id(fieldset_id)

    def click(self):
        btn = self.fieldset_obj.find_element_by_class_name('x-tool-toggle')
        btn.click()

    def is_collapsed(self):
        cls = self.fieldset_obj.get_attribute('class')
        if 'collapsed' in cls:
            return True
        else:
            return False


class GridContextMenu(object):
    u"""
    Класс для работы с контекстным меню грида
    """

    def __init__(self, webdriver, elem_xpath):
        self.driver = webdriver
        self.context_menu_object = webdriver.find_element_by_xpath(elem_xpath)
        self.id = self.context_menu_object.get_attribute('id')

    @classmethod
    def get_visible_menu(cls, webdriver):
        elem_xpath = """
            //div[contains(@class, 'x-menu') and
            contains(@class, 'x-menu-floating') and
            contains(@style, 'visibility: visible')]"""
        return GridContextMenu(webdriver, elem_xpath)

    def get_button_id(self, button_name):
        b_id = self.driver.execute_script(u"""
            var m = Ext.getCmp('{menu_id}');
            b = m.find('text', '{b_name}');
            return b!== undefined ? b[0].id : false;
        """.format(menu_id=self.id, b_name=button_name))
        assert b_id, u'Button does not exists!'
        return b_id

    def click_by_button(self, button_name):
        button_id = self.get_button_id(button_name)
        self.context_menu_object.find_element_by_id(button_id).click()

    def has_button(self, button_name):
        return bool(self.get_button_id(button_name))
