# -*- coding: utf-8 -*-
"""
В данном файле хранятся фун. для интеграции behave с testlink. Для
выполнения тест плана необходимо у сценариев указать их id в testlink в
виде тегов (например esch-56, сценариям предназначем
для создания зависимостей которых нету
в testlink нужно указать тег required)
и затем запустить behave c параметрами:
    PROJECT_NAME
    TESTPLAN_NAME
    BUILD_NAME

    Пример:
    behave --lang ru features/ -D PROJECT_NAME='PROJECT NAME'
        -D TESTPLAN_NAME='TESTPLAN NAME' -D BUILD_NAME="BUILD NAME"
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import testlink

from functools import wraps
from testlink.testlinkerrors import TLResponseError
import six

# url api тестлинка
TESTLINK_API_URL = 'http://testms.bars-open.ru/lib/api/xmlrpc/v1/xmlrpc.php'

# ключ для подключения к api тестлинка
TESTLINK_API_KEY = '5b5ce143b5de8f6a2ed33d6e6bcb553b'

BEHAVE_TO_TESTLINK_STAUTS = {
    'passed': 'p',
    'failed': 'f',
    'skipped': 'b',
    'untested': 'n'
}

TESTLINK_PARAMS = ('PROJECT_NAME', 'TESTPLAN_NAME', 'BUILD_NAME')


def setup_tsl_var(context, project_name, testplan_name, build_name):
    u"""
    Получаем инфо. о тестплане, id билда тест плана и список тест кейсов
    для выполнения.
    """
    context.tsl = testlink.TestlinkAPIClient(
        TESTLINK_API_URL,
        TESTLINK_API_KEY
    )
    try:
        context.testplan_info = context.tsl.getTestPlanByName(
            project_name,
            testplan_name
        )[0]
    except TLResponseError as tl_err:
        print(tl_err.code)

    testplan_builds = context.tsl.getBuildsForTestPlan(
        context.testplan_info['id']
    )
    for build in testplan_builds:
        if build['name'] == build_name:
            context.testplan_buildid = build['id']
            break

    testcases_info = context.tsl.getTestCasesForTestPlan(
        context.testplan_info['id']
    )

    context.testcases_id = {v[0]['full_external_id']: k
                            for k, v
                            in six.iteritems(testcases_info)}


def send_report_to_tsl(context, scenario):
    u"""
    Формируем сообщение о прохождение сценария и отправляем в тестлинк.
    В случае если тест кейс провалился (стаутс failed) и в котнексте сохранен
    путь к скрншоту (context.screen_shot_path) то данный скриншот будет
    прикреплен к отчету о выполнении.
    """
    external_id = (set(scenario.tags) & set(context.testcases_id.keys())).pop()
    msg = 'Scenario passed.'
    if scenario.status == 'failed':
        msg = u'Scenario failed at step "{}".'.format(
            context.failed_step
        )
    elif scenario.status == 'skipped':
        msg = 'Scenario skipped.'

    res = context.tsl.reportTCResult(
        testplanid=context.testplan_info['id'],
        status=BEHAVE_TO_TESTLINK_STAUTS[scenario.status],
        testcaseexternalid=str(external_id),
        buildid=context.testplan_buildid,
        notes=msg
    )
    if hasattr(context, 'screen_shot_path') and scenario.status == 'failed':
        a_file = open(context.screen_shot_path, 'rb')
        context.tsl.uploadExecutionAttachment(
            a_file, executionid=res[0]['id'], title='Screen shot of error',
            description='Screen shot of error.')


def testlink_setup(function):
    u"""
    Декоратор для фун. before_all из файла environment,
    для инициализации testlinkapi.
    """
    @wraps(function)
    def wrapper_testlink_setup(arg):
        if set(TESTLINK_PARAMS).issubset(arg.config.userdata):
            setup_tsl_var(
                arg,
                project_name=arg.config.userdata['PROJECT_NAME'],
                testplan_name=arg.config.userdata['TESTPLAN_NAME'],
                build_name=arg.config.userdata['BUILD_NAME']
            )
            arg.execute_all = False
        else:
            arg.execute_all = True
            arg.testcases_id = {}
        function(arg)
    return wrapper_testlink_setup


def scenario_execute(function):
    u"""
    Декоратор для фун. before_scenario, на основе тест плана определяет
    выполнять сценарий или нет.
    """
    @wraps(function)
    def wrapper_scenario_execute(arg_context, arg_scenario):
        scenario_in_testplan = (
            set(arg_scenario.tags) & set(arg_context.testcases_id.keys())
            or 'required' in arg_scenario.tags)
        if not scenario_in_testplan and not arg_context.execute_all:
            arg_scenario.skip()
        function(arg_context, arg_scenario)
    return wrapper_scenario_execute


def send_report(function):
    u"""
    Декоратор для фун. after_scenario, если сценарий в тестплане то отправляет
    инф. о его выполнении в testlink
    """
    @wraps(function)
    def wrapper_send_report(arg_context, arg_scenario):
        if (set(arg_scenario.tags) & set(arg_context.testcases_id.keys())
                and not arg_context.execute_all):
            send_report_to_tsl(arg_context, arg_scenario)
        function(arg_context, arg_scenario)
    return wrapper_send_report


def skip_feature(context, feature, required_tags=None):
    u"""
    Функция для определения нужно ли выполнять feature файл в текущем
    тест плане. Операция производиться путем сравнения id-шников тест кейсов
    из тест плана и feature файла, если есть пересечение то features
    файл будет выполнен. Предполагается что данная функция будет вызваться
    в hook'е before_feature.

    :param context: Behave объект context хранит контекстную информацию
     во время выполнения тестов. В данном случае во время выполнения тест плана
     в context сохранены id-шники тестов из тест плана (context.testcases_id)
    :param feature: Объект описывающий feature файл.
    :param required_tags: Список дополнительных тегов для тест кейсов которые
     необходимо включить для выполнения в тест план.

    :type required_tags: list
    :type feature: behave.model.Feature

    :return: True если feature файл будет пропущен иначе False.
    """
    if context.testcases_id:
        feature_tags = [t for scenario in feature.scenarios
                        for t in scenario.tags]

        testplan_tags = list(context.testcases_id.keys())
        if required_tags and isinstance(required_tags, list):
            testplan_tags += required_tags

        if not (set(feature_tags) & set(testplan_tags)):
            feature.skip()
            return True
        return False

    return False
