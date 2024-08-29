# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals

from functools import wraps
from jira import JIRA
from jira import JIRAError

STATUS_TO_TEST = (u'Закрыт', u'Реализован', u'Приемка', None)
BARS_JIRA_URL = 'https://jira.bars.group'


def auth_jira(username, password, server=BARS_JIRA_URL):
    u"""
    Возращает авторизованую сессию в jira.
    :param username: Логин пользователя
    :param password: Пароь пользователя
    :param server: url адресс сервера jira
    :rtype: JIRA
    """
    return JIRA(basic_auth=(username, password), server=server)


def get_status(context, issue_id):
    u"""
    :param context: контекст behave`а
    :param issue_id: id задачи в jira
    :return: Статус задачи
    :rtype: str
    """
    try:
        issue = context.jira_session.issue(issue_id, fields='status')
        return issue.fields.status.name
    except JIRAError:
        return None


def jira_check(func):
    """
    Декоратор для проверки статуса задачи.
    Если задача не закрыта, то сценарий будет пропущен.
    Применяется для функции before_scenario из environment.py.
    """
    @wraps(func)
    def wrapper(context, scenario):

        if not context.config.userdata.getbool('JIRA', False):
            func(context, scenario)
        else:
            need_skip = False
            for tag in scenario.tags:
                tag = tag.upper()
                if tag.startswith('EDU'):
                    if tag not in list(context.issues.keys()):
                        context.issues[tag] = get_status(context, tag)
                    if context.issues[tag] not in STATUS_TO_TEST:
                        need_skip = True
            if need_skip:
                # Тэг no-ui добавляется, что бы не инициализировался браузер
                # для пропускаемого сценария.
                scenario.tags.append('no-ui')
                scenario.skip()
            func(context, scenario)

    return wrapper
