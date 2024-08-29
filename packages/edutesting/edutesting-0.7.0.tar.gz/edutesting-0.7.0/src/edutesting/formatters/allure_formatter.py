# coding: utf-8
u"""
Адаптер для отчетов yandex.allure

TODO:
    * Добавить для тест кейсов простановку их приоритета
    * Добавить возможность добавлять приложения с типом txt, xml
    * Решить проблему с отображением точек в назвниях шагов, тест кейсов
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import os
import uuid
from csv import DictReader
from xml.etree import ElementTree as ET

from behave.formatter.base import Formatter
from behave.model import ScenarioOutline
from behave.model_core import Status

from .helpers import replace_dots
from .helpers import IMAGE
from .helpers import HTML
import six

FAILED = Status.failed


class AllureFormatter(Formatter):
    u"""
    Класс генерирует xml отчеты совместимые с yandex.allure
    EXAMPLE:
        "behave features/
        --format=edutesting.formatters:allure_formatter:AllureFormatter
        -D env_conf=/path/to/dir/env_conf.csv
        -D allure_dir=/path/to/dir/reports
        "
    """

    name = "allure.report"
    description = "Make xml reports for yandex.allure"
    _feature = None
    _reports_dir = None

    def __init__(self, stream_opener, config):
        super(AllureFormatter, self).__init__(stream_opener, config)

        self._reports_dir = self.config.userdata.get(
            'allure_dir', self.config.base_dir)

        if not os.path.exists(self._reports_dir):
            os.makedirs(self._reports_dir)

    def _environment(self):
        u"""
        Создание xml отчета с информацией о тестовой среде. Формируется на
        основе данных из файла переданных при запуске в параметре env_config.
        Файл должен быть в csv формате следующего вида.
        EXAMPLE:
            web_edu,project,project
            localhost,hostname,hostname
            1.31,project_version,project_version
        """
        env_conf_path = self.config.userdata.get('env_config', None)
        if env_conf_path:
            assert os.path.exists(env_conf_path), (
                u"File with environment variables don't exists!"
            )
            f = open(env_conf_path)
            reader = DictReader(f, ('value', 'name', 'key'))
            environment = ET.Element(u'environment')
            name = ET.SubElement(environment, u'name')
            name.text = u'Тестовое окружение:'

            for row in reader:
                param = ET.Element(u'parameter')
                value = ET.SubElement(param, u'value')
                value.text = row['value']
                name = ET.SubElement(param, u'name')
                name.text = row['name']
                key = ET.SubElement(param, u'key')
                key.text = row['key']
                environment.append(param)

            path = os.path.join(self._reports_dir, u'environment.xml')
            f = open(path, 'w+')
            f.write(ET.tostring(environment))
            f.close()

    def feature(self, feature):
        self._feature = feature

    def _write(self, suite):
        u"""
        Создает файл с xml отчетом.
        :return:
        """
        filename = u'-'.join((str(uuid.uuid4()), u'testsuite.xml'))
        path = os.path.join(self._reports_dir, filename)
        f = open(path, 'wb+')
        f.write(ET.tostring(suite))
        f.close()

    def _process_step(self, scenario_step):
        u"""
        Формирует xml элемент с информацией о шаге сценария.
        :param scenrio_step: behave Step instance
        :return: xml Element
        """
        step = ET.Element(u'step')
        if hasattr(scenario_step, 'start'):
            step.set(u'start', scenario_step.start)
        if hasattr(scenario_step, 'stop'):
            step.set(u'stop', scenario_step.stop)
        step.set(u'status', scenario_step.status.name)

        name = ET.SubElement(step, u'name')
        name.text = replace_dots(
            u' '.join((scenario_step.keyword, scenario_step.name, ))
        )

        if (scenario_step.status == FAILED and
                hasattr(scenario_step, 'attachment')):
            attachs = ET.SubElement(step, u'attachments')
            screen = ET.SubElement(attachs, u'attachment')
            screen.set(u'title', u'Приложение:')
            screen.set(u'source', scenario_step.attachment)
            if scenario_step.attachment.endswith(IMAGE):
                screen.set(u'type', u'image/png')
            elif scenario_step.attachment.endswith(HTML):
                screen.set(u'type', u'html')
            else:
                screen.set(u'type', u'txt')


        return step

    def _failed_step_info(self, scenario):
        u"""
        Возвращает информацию о у шаге на котором произошло падение сценария.
        :param scenario: behave Scenario instance
        :return:
        """
        info = {}
        for s in scenario.all_steps:
            if s.status == FAILED:
                info['message'] = getattr(
                    s, 'error_message', u'No error message probided')
                stack_trace = getattr(
                    s, 'exception', u'No stack trace provided')
                if not isinstance(stack_trace, six.string_types):
                    stack_trace = six.text_type(stack_trace)
                info['stack-trace'] = stack_trace
        return info

    def _process_scenario(self, scenario):
        u"""
        Формирует xml элемент с информацией о тест кейсе.
        :param scenario: behave Scenario instance
        :return: xml Element
        """
        test_case = ET.Element(u'test-case')
        if hasattr(scenario, 'start'):
            test_case.set(u'start', scenario.start)
        if hasattr(scenario, 'stop'):
            test_case.set(u'stop', scenario.stop)
        test_case.set(u'status', scenario.status.name)

        name = ET.SubElement(test_case, u'name')
        name.text = replace_dots(scenario.name)

        steps = ET.SubElement(test_case, u'steps')

        for s in scenario.all_steps:
            step = self._process_step(s)
            steps.append(step)

        if hasattr(scenario, 'examples'):
            params = ET.SubElement(test_case, u'parameters')
            for example in scenario.examples:
                row = example.table[example.index]
                for h in row.headings:
                    param = ET.Element(u'parameter')
                    name = ET.SubElement(param, u'name')
                    name.text = h
                    value = ET.SubElement(param, u'value')
                    value.text = row.get(h)
                    kind = ET.SubElement(param, u'kind')
                    kind.text = u'argument'
                    params.append(param)

        if self._feature.description:
            description = ET.SubElement(test_case, u'description')
            description.text = u' '.join(self._feature.description)

        if scenario.status == FAILED:
            fail_info = self._failed_step_info(scenario)
            failure = ET.SubElement(test_case, u'failure')
            if fail_info:
                msg = ET.SubElement(failure, u'message')
                msg.text = fail_info[u'message']
                trace = ET.SubElement(failure, u'stack-trace')
                trace.text = fail_info[u'stack-trace']

        return test_case

    def _process_feature(self, feature):
        u"""
        Формирует xml элемент с информацией о тест сьюте.
        :param scenario: behave Scenario instance
        :return: xml Element
        """
        suite = ET.Element(u'test-suite')
        if hasattr(feature, 'start'):
            suite.set(u'start', feature.start)
        if hasattr(feature, 'stop'):
            suite.set(u'stop', feature.stop)

        name = ET.SubElement(suite, u'name')
        name.text = replace_dots(self._feature.name or self._feature.filename)
        labels = ET.SubElement(suite, u'labels')
        f_label = ET.SubElement(labels, u'label')
        f_label.set(u'name', u'feature')
        f_label.set(u'value', self._feature.name)
        f_lang = ET.SubElement(labels, u'label')
        f_lang.set(u'name', u'language')
        f_lang.set(u'value', u'ru')

        if self._feature.description:
            description = ET.SubElement(suite, u'description')
            description.text = u' '.join(self._feature.description)
            f_story = ET.SubElement(labels, u'label')
            f_story.set(u'name', u'story')
            f_story.set(u'value', description.text)

        test_cases = ET.SubElement(suite, u'test-cases')
        for scenario in self._feature.scenarios:
            if isinstance(scenario, ScenarioOutline):
                for s in scenario.scenarios:
                    test_case = self._process_scenario(s)
                    test_cases.append(test_case)
            else:
                test_case = self._process_scenario(scenario)
                test_cases.append(test_case)

        return suite

    def eof(self):
        self._environment()
        suite = self._process_feature(self._feature)
        self._write(suite)
