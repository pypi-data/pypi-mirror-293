# Кастомизация под проект:
1. добавляем в settings
OBJECTPACK_BASE_TEST = 'ssuz.apply_tests.base_test.BaseTest'
в базовый класс уобно добавлять какие-либо константы, использующие уже в интеграционных тестах:

from objectpack_integration_test.base_test import BaseTest as ObjectpackBaseTest


class BaseTest(ObjectpackBaseTest):
    """
    Перегруженный класс для всех видов тестрования
    """
    user_id = 1
    unit_id = 3  # 47
    user_config = {'login_login': 'admin', 'login_password': 'admin'}
    change_permissions = False

    # пак только для определнных пользователей
    # если атрибут включен, все экшены должны прийти с зарпетом доступа
    all_access_denied = False

2. добавляем в settings
OBJECTPACK_BASE_INTEGRATION_TEST = 'ssuz.apply_tests.integration_test.BaseIntegrationTest'

пример реализации
from objectpack_integration_test.integration_test import BaseIntegrationTest as ObjectpackBaseIntegrationTest

from ssuz.controllers import obs
from ssuz.unit.models import Unit
from ssuz.users.role.models import RolePermission, Role

from .base_test import BaseTest
from . import helpers


class BaseIntegrationTest(ObjectpackBaseIntegrationTest):
    """
    Перегруженный класс интеграционных тестов
    """
    period_id = 1
    in_login = False

    def setUp(self):
        """
        Предустановка значений для теста
        """
        super(BaseIntegrationTest, self).setUp()

        if not self.in_login:
            # авторизация
            response = self.client_session.post(
                '/auth/login',
                self.user_config)

            self.check_status(response)

            if self.change_permissions:
                # чтобы поставить ОУ, должны быть права на чтение ОУ
                role = Role.objects.get(name=self.user_config['login_login'])
                from ssuz.permissions import PERM_UNIT_VIEW
                RolePermission.objects.get_or_create(
                    role=role,
                    permission=PERM_UNIT_VIEW
                )
            # ставим ОУ
            response = self.client_session.post(
                '/actions/units/set_current_unit',
                {'unit_id': self.unit_id})

            self.check_status(response)
            self.in_login = True

        self.condition.update({Unit: self.unit_id})

    @classmethod
    def get_pack_instance(cls, pack_class):
        """
        В зависимости от используемых технологий, необходимо перегрузить
        получение экземпляра пака или через Observer или m3.actions.url

        :param pack_class: pack_class
        :return: instanse of pack
        """
        return obs.get_pack_instance(pack_class.get_short_name())

    @classmethod
    def get_list_pack_from_observer(cls):
        """
        Необходим для проверки _is_primary_for_model
        Возвращает список всех зарегистрованных паков
        можно взять из Observer: obs._model_register.values()

        :return: список зарегистрованных паков
        :rtype: list
        """
        return obs._model_register.values()

    def post_and_get_response(self, url, context):
        """
        Отправляет POST-запрос и возвращает response ответ

        :param url: строка с адресом
        :type url: str
        :param context: Контекст
        :type context: dict
        :return: response
        """
        можно перегрузить данные метод и сделат проверку прав.
        например удалять все права и убедиться, что по url вернется "у вас нет прав". Затем включить права и проверить уже работу логики.
        Данный подход реализован в БАРС.Электронный Колледж

Если есть необходимость прогонять тесты под разными пользователями, то добавлем Mixin.
Необходимость такая может появиться, если меняется логика поведения в зависимости от ролей.
Например студенты, которые имеют доступ в личный кабинет, но приэтом остаются обычне django.User и могут сделать запрос по прямому url в систему.

class SuperAdminMixin(object):
    """
    mixin для авторизации Админа ОУ
    """
    unit_id = 3
    user_config = {
        'login_login': 'dev_test_unit_admini',
        'login_password':
        'dev_test_unit_admini'
    }
    change_permissions = True


Стандартный набор тестов для пака на основе ObjectPack, кладем в app/tests.py, тесты стартанут, если есть файл models.py и app

import objectpack_integration_test
from ssuz import apply_tests
from actions import Pack


class TestCaseUnit(objectpack_integration_test.BaseUnitTestModel):
    """
    Юнит тест пака
    атрибут класса pack инстанс Objectpack
    """
    pack = Pack()


class TestCaseIntegration(apply_tests.BaseIntegrationTestPack):
    """
    Интеграционный тест пака, под пользователем с ролью SuperAdmin
    атрибут класса pack_class, класс-наследник Objectpack
    """
    pack_class = Pack


class SuperAdminTestCaseIntegration(
        apply_tests.SuperAdminMixin,
        TestCaseIntegration
):
    """
    Интеграционный тест пака, под пользователем с ролью AdminOU
    атрибут класса pack_class, класс-наследник Objectpack
    """


# Runnerы

Перегружаем раннер джанговский, в устновку БД можем добавить создание пользователей, загрузку первичный фикстур
TEST_RUNNER = 'testing.DatabaselessTestRunner'
Надо помнить, что для jenkins свой Runner, его также надо перегружать
JENKINS_TEST_RUNNER = 'testing.JenkinsDatabaselessTestRunner'
