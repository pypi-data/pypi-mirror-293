# -*- coding: utf-8 -*-
"""
Набор интеграционных тестов
BaseIntegrationTest - Базовый класс интеграционных тестов
BaseIntegrationSimplePackTest - тесты для objectpack.BasePack
BaseIntegrationTestPack - тесты для objectpack.ObjectPack
BaseIntegrationTreeTestPack - тесты для BaseTreeDictionaryModelActions
"""
from __future__ import absolute_import
from __future__ import unicode_literals

import copy
import json
import uuid
import os

from django.test.client import Client
from django.conf import settings

from m3.actions import ControllerCache
from m3.actions import _import_by_path

from objectpack.slave_object_pack import SlavePack

from .helpers import PackValueForContext
from .helpers import ModelValueForContext
from .helpers import gen_uniq
from .helpers import GMWindowField
from .base_test import BaseTest
import six

path = getattr(settings, 'OBJECTPACK_BASE_TEST', None)
if path:
    PATCHED_BASE_TEST = _import_by_path(path)
else:
    PATCHED_BASE_TEST = BaseTest


class BaseIntegrationTest(PATCHED_BASE_TEST):
    """
    Базовый класс интеграционных тестов
    Внутри есть проверка офрографиии self.check_spell(word)
        и клиент self.client_session для post/get запросов
    """

    pack = None  # instance
    pack_class = None  # class
    context_declaration = {}

    def __init__(self, *args, **kwargs):
        super(BaseIntegrationTest, self).__init__(*args, **kwargs)

        ControllerCache.populate()

        # Атрибуты пака (Названия Экшенов) - окна на проверку
        self.windows_actions = []
        # Атрибуты пака (Названия Экшенов) - данные на проверку
        self.rows_actions = []
        self.context = {}  # Контекс для post

        self.good_save_action = None

        self.period_id = 1

        self.condition = {}  # фильтры для моделей в БД

        self.exclude_actions = []  # исключения для test_all_actions

        self.client_session = Client()

        self.ACCEPTED_STATUSES_CODES = (200,)

        self.log_path = os.path.join(
            settings.LOG_PATH, 'integration_tests_log')
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)

    def setUp(self):
        """
        Предустановка значений
        """
        super(BaseIntegrationTest, self).setUp()

    def check_status(self, response):
        """
        Провека кодов возврата http ответов

        :param response: http ответ от сервера
        """
        if response.status_code not in self.ACCEPTED_STATUSES_CODES:
            f_name = os.path.join(self.log_path, str(uuid.uuid4()))
            f = open(f_name, 'w')
            f.write(response.content)
            f.close()
            self.assertIn(response.status_code, self.ACCEPTED_STATUSES_CODES, (
                'Status code is {0}. Error logged in {1} file'.format(
                    response.status_code, f_name)))

    def check_row(self, rows):
        """
        Вспомогательная ф-я, проверяет ключи total, rows в JSON

        :param rows: json, который требует валидации
        :type rows: json
        :return: результат проверки
        :rtype: bool
        """
        if "total" not in rows or "rows" not in rows:
            if "message" in rows:
                self.assertTrue(
                    self.check_spell(rows["message"]),
                    rows["message"]
                )
                return False

        self.assertTrue("total" in rows)
        self.assertTrue("rows" in rows)
        return True

    def post_and_get_json(self, url, context):
        """
        Отправляет POST-запрос и возвращает json

        :param url: строка с адресом
        :type url: str
        :param context: Контекст
        :type context: dict
        :return: response
        :rtype: json
        """
        response = self.post_and_get_response(url, context)

        rows = json.loads(response.content)

        return response, rows

    def post_and_get_response(self, url, context):
        """
        Отправляет POST-запрос и возвращает response ответ

        :param url: строка с адресом
        :type url: str
        :param context: Контекст
        :type context: dict
        :return: response
        """
        response = self.client_session.post(url, context)
        self.check_status(response)

        return response

    def get_value_for_context(self, key, val):
        """
        Получить значение из БД. По key ищем id_param_name в паках
        и достаем первый попавшийся id у объекта модели пака

        :param key: имя параметра, для которого необходимо
            сгенерировать/найти данные
        :param val: type of key
        :return: genereated object
        """
        condition = {}
        condition.update(self.condition)

        if (hasattr(self.pack, 'model') and
                hasattr(self.pack, 'id_param_name') and
                self.pack.id_param_name == key):
            res = ModelValueForContext(
                model=self.pack.model,
                condition=condition, gm=True
            ).get()
        else:
            res = PackValueForContext(
                key=key,
                val=val,
                condition=condition, gm=True
            ).get()
        return res

    @classmethod
    def get_pack_instance(cls, pack_class):
        """
        В зависимости от используемых технологий, необходимо перегрузить
        получение экземпляра пака или через Observer или m3.actions.url

        :param pack_class: pack_class
        :return: instanse of pack
        """
        raise NotImplementedError()

    @classmethod
    def get_list_pack_from_observer(cls):
        """
        Необходим для проверки _is_primary_for_model
        Возвращает список всех зарегистрованных паков
        можно взять из Observer: obs._model_register.values()

        :return: список зарегистрованных паков
        :rtype: list
        """
        return []


path = getattr(settings, 'OBJECTPACK_BASE_INTEGRATION_TEST', None)
if path:
    PATCHED_BASE_INTEGRATION_TEST = _import_by_path(path)
else:
    PATCHED_BASE_INTEGRATION_TEST = BaseIntegrationTest


class BaseIntegrationSimplePackTest(PATCHED_BASE_INTEGRATION_TEST):
    """
    Набор интеграционных тестов пака, на основе objectpack.BasePack
    """
    def __init__(self, *args, **kwargs):
        """
        Инициализация созданого объекта
        """
        super(BaseIntegrationSimplePackTest, self).__init__(*args, **kwargs)

        if not self.pack_class:
            raise NotImplementedError()

        self.pack = self.get_pack_instance(self.pack_class)

        if not self.pack:
            raise NotImplementedError(self.pack_class)

    def post_and_get_grid_json(self, action, context):
        """
        Отправляет POST-запрос и возвращает (response, json)
        json check total and rows in json

        :param action: экшн (вьюха)
        :type action: objectpack.BaseAction
        :param context: Контекст
        :type context: dict
        :return: (response, json)
        """

        go_context = copy.copy(context)
        self.get_acd(action, go_context)

        response, rows = self.post_and_get_json(
            action.get_absolute_url(), go_context)

        self.check_row(rows)
        return response, rows

    def get_acd(self, action, context):
        """
        Обновляет контекст, согласно declare_context или context_declaration

        :param action: экшн (вьюха)
        :type action: objectpack.BaseAction
        :param context: Контекст
        :type context: dict
        """
        acd = []
        if hasattr(action, 'context_declaration'):
            acd = action.context_declaration()

        if self.context_declaration and isinstance(acd, dict):
            acd.update(self.context_declaration)

        if acd:
            if isinstance(acd, dict):
                for key, val in six.iteritems(acd):
                    if key not in context:
                        res = self.get_value_for_context(key, val)
                        if res:
                            context[key] = res
            if isinstance(acd, list):
                for j in acd:
                    if j.name not in context:
                        res = self.get_value_for_context(
                            j.name, {'type': j.type}
                        )
                        if res:
                            context[j.name] = res

    def test_windows_actions(self):
        """
        Тест проверки вызова окон
        """
        for action_attr in self.windows_actions:
            action = getattr(self.pack, action_attr, None)

            self.setUp()
            context = copy.copy(self.context)

            if 'new_window_action' == action_attr:
                acd = self.pack.declare_context(action)
                if self.pack.id_param_name in acd:
                    context[self.pack.id_param_name] = ''

            self.get_acd(action, context)

            if action:
                try:
                    self.post_and_get_response(
                        action.get_absolute_url(),
                        context
                    )
                except Exception as ex:
                    ex.args = (ex.args if ex.args else tuple()) + (action,)
                    raise

    def test_rows_actions(self):
        """
        Тест получает все значения из Пака
        """
        for action_attr in self.rows_actions:
            action = getattr(self.pack, action_attr, None)

            self.setUp()
            context = copy.copy(self.context)

            try:
                _, rows = self.post_and_get_grid_json(
                    action,
                    context
                )
            except Exception as ex:
                ex.args = (ex.args if ex.args else tuple()) + (action,)
                raise

            if 'rows' in rows:
                self.assertEqual(len(rows["rows"]), rows["total"], action)
            else:
                self.assertFalse(rows["success"], action)

    def another_save_action(self, win, save_action, context):
        """
        Отправляет пост на save_action, с дополнительным контекстом context
        и с парсенными данными win

        :param objectpack.ObjectPack pack: инстанс пака
        :param objectpack.BaseEditWindow win: инстанс окна
        :param objectpack.dict context: инстанс окна
        """
        context = GMWindowField(self.pack, win, context, self.condition).get()

        self.get_acd(save_action, context)

        context = gen_uniq(
            context,
            self.pack.model,
            self.condition
        )

        self.post_and_get_response(
            save_action.get_absolute_url(),
            context
        )


class BaseIntegrationTestPack(BaseIntegrationSimplePackTest):
    """
    Набор интеграционных тестов пака, на основе objectpack.ObjectPack
    """
    def __init__(self, *args, **kwargs):
        """
        Инициализация созданого объекта
        """
        super(BaseIntegrationTestPack, self).__init__(*args, **kwargs)
        # setUp срабатывает несколько раз за instance
        if self.pack.add_window and not self.pack.read_only:
            self.windows_actions.append('new_window_action')

        if self.pack.edit_window and not self.pack.read_only:
            self.windows_actions.append('edit_window_action')

        if self.pack.list_window:
            self.windows_actions.append('list_window_action')

        if self.pack.select_window:
            self.windows_actions.append('select_window_action')

        if not self.good_save_action:
            save_action = getattr(self.pack, 'save_action', None)
            self.good_save_action = save_action

    def test_limit_row_pack(self):
        """
        Тест получает значения с ограничеием (пагинация)
        """
        if getattr(self.pack, 'allow_paging', None):
            rows_action = getattr(self.pack, 'rows_action', None)

            context_new = copy.copy(self.context)
            context_new['limit'] = 25
            context_new['start'] = 0

            _, rows = self.post_and_get_grid_json(
                rows_action,
                context_new
            )
            if "rows" in rows:
                self.assertTrue(len(rows["rows"]) <= 25)

    def test_filter_row_pack(self):
        """
        Тест получает значения по фильтру
        """
        rows_action = getattr(self.pack, 'rows_action', None)

        context_new = copy.copy(self.context)

        need_filter = False
        for row in self.pack.columns:
            if 'searchable' in row and row['searchable']:
                need_filter = True
                break

        if need_filter:
            context_new['filter'] = '123'

            self.post_and_get_grid_json(
                rows_action,
                context_new
            )

    def test_order_row_pack(self):
        """
        Тест проверяет сортировку по всем полям column в Паке
        """
        rows_action = getattr(self.pack, 'rows_action', None)

        context_new = copy.copy(self.context)

        for row in self.pack.columns:
            # Проверяем включен ли атрибут сортировки у колонки
            if row.get('sortable', None):
                context_new['sort'] = row['data_index']
                context_new['dir'] = 'ASC'

                self.post_and_get_grid_json(
                    rows_action,
                    context_new
                )

                context_new['sort'] = row['data_index']
                context_new['dir'] = 'DESC'

                self.post_and_get_grid_json(
                    rows_action,
                    context_new
                )

    def test_all_actions(self):
        """
        Тестируем все экшены, которые не тестируются другими тестами
        """
        actions = self.pack.actions

        # убираем actionы, которые уже тестируются в других местах
        for i in self.rows_actions:
            action = getattr(self.pack, i)
            if action in actions:
                actions.remove(action)

        for i in self.windows_actions:
            action = getattr(self.pack, i)
            if action in actions:
                actions.remove(action)

        for attr_name in ['delete_action', 'save_action', 'rows_action']:
            action = getattr(self.pack, attr_name)
            if action in actions:
                actions.remove(action)

        edit_window_action = getattr(self.pack, 'edit_window_action')
        if edit_window_action and edit_window_action in actions:
            actions.remove(edit_window_action)

        list_window_action = getattr(self.pack, 'list_window_action')
        if list_window_action and list_window_action in actions:
            actions.remove(list_window_action)

        select_window_action = getattr(self.pack, 'select_window_action')
        if select_window_action and select_window_action in actions:
            actions.remove(select_window_action)

        # неверные кастомные экшены, от них надо злостно избавляться!
        save_window_action = getattr(self.pack, 'save_window_action', None)
        if save_window_action and select_window_action in actions:
            actions.remove(save_window_action)

        for attr_name in self.exclude_actions:
            action = getattr(self.pack, attr_name, None)
            if action in actions:
                actions.remove(action)

        for action in actions:
            self.setUp()
            context = copy.copy(self.context)

            self.get_acd(action, context)

            try:
                if action:
                    self.post_and_get_response(
                        action.get_absolute_url(),
                        context
                    )
            except Exception as ex:
                ex.args = (ex.args if ex.args else tuple()) + (action,)
                raise

    def test_delete_action(self):
        """
        Тест на удаление с указанием id объекта
        """
        # получаем action для удаления
        if hasattr(self.pack, 'can_delete'):
            delete_action = getattr(self.pack, 'delete_action', None)
            if delete_action:
                context = copy.copy(self.context)

                self.get_acd(delete_action, context)

                self.post_and_get_response(
                    delete_action.get_absolute_url(),
                    context)

    def test_good_add_save_action(self):
        """
        Тестируем сохранени хороших данных, т.е. успешное сохранение
        """
        if self.good_save_action:
            add_window = getattr(self.pack, 'add_window', None)
            if add_window:
                aw = add_window

                if isinstance(self.pack, SlavePack):
                    try:
                        instance_aw = aw(model=self.pack.model)
                    except TypeError:
                        instance_aw = aw()
                else:
                    instance_aw = aw()

                context_new = copy.copy(self.context)

                context_new[self.pack.id_param_name] = 0

                self.another_save_action(
                    instance_aw,
                    self.good_save_action,
                    context_new
                )

    def test_is_primary_for_model(self):
        """
        Проверка сущестования
        одного и только одного пака с _is_primary_for_model=True
        """
        list_of_packs = self.get_list_pack_from_observer()

        if list_of_packs:
            # Если пак первичный, то больше не должно быть таких
            if self.pack._is_primary_for_model:
                for pack in list_of_packs:
                    if hasattr(pack, 'model'):
                        self.assertFalse(
                            (self.pack != pack) and
                            (self.pack.model == pack.model) and
                            pack._is_primary_for_model, 'double primary pack')
            # если пак вторичный, то где-то должен быть первичный
            else:
                is_prime = False
                for pack in list_of_packs:
                    if hasattr(pack, 'model'):
                        if self.pack.model == pack.model and\
                            self.pack != pack and\
                                hasattr(pack, '_is_primary_for_model'):
                            is_prime = is_prime or pack._is_primary_for_model
                self.assertTrue(is_prime, 'no primary pack')


class BaseIntegrationTreeTestPack(BaseIntegrationSimplePackTest):
    """
    набор тестов для паков на основе BaseTreeDictionaryModelActions
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализация созданого объекта
        """
        super(BaseIntegrationTreeTestPack, self).__init__(*args, **kwargs)
        window = getattr(self.pack, 'edit_node_window', None)
        if window:
            self.windows_actions.extend([
                'new_node_window_action',
                'edit_node_window_action',
            ])

        self.windows_actions.extend([
            'list_window_action',
            'select_window_action',
            'edit_grid_window_action'

            # не окна, но пофиг
            'delete_node_action',
            # 'delete_row_action'  # not used

            'node_action',
            'row_action',
            'nodes_like_rows_action',
            # 'last_used_action',
        ])

    def test_node_pack(self):
        """
        тест для получения всех нод
        """
        nodes_action = getattr(self.pack, 'nodes_action', None)
        self.post_and_get_response(
            nodes_action.get_absolute_url(),
            self.context
        )

    def test_filter_row_pack(self):
        """
        тест для получения и фльтрации данных
        """
        rows_action = getattr(self.pack, 'rows_action', None)
        context_new = copy.copy(self.context)
        context_new['filter'] = '12'
        self.post_and_get_response(
            rows_action.get_absolute_url(),
            context_new
        )

    def test_new_grid_window_action(self):
        """
        тестируем новое окно
        """
        window = getattr(self.pack, 'edit_window', None)
        if window:
            action = getattr(self.pack, 'new_grid_window_action', None)
            context_new = copy.copy(self.context)
            context_new[self.pack.contextTreeIdName] = 0
            context_new['id'] = 0

            self.get_acd(action, context_new)

            self.post_and_get_response(
                action.get_absolute_url(),
                context_new
            )

    def test_save_node_action(self):
        """
        Тестируем сохранени хороших данных, т.е. успешное сохранение
        save_action
        """
        save_action = getattr(self.pack, 'save_node_action', None)
        if save_action:
            # hack by helpers
            self.pack.model = self.pack.tree_model
            context_new = copy.copy(self.context)

            window = getattr(self.pack, 'edit_node_window', None)
            if window:
                self.another_save_action(
                    window(),
                    save_action,
                    context_new
                )

    def test_save_row_action(self):
        """
        Тестируем сохранени хороших данных, т.е. успешное сохранение
        save_action
        """
        save_action = getattr(self.pack, 'save_row_action', None)
        if save_action:
            # hack by helpers
            self.pack.model = self.pack.tree_model
            context_new = copy.copy(self.context)

            window = getattr(self.pack, 'edit_window', None)
            if window:
                self.another_save_action(
                    window(),
                    save_action,
                    context_new
                )
