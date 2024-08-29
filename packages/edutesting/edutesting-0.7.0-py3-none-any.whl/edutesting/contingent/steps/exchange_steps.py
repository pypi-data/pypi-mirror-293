# coding: utf-8

from __future__ import absolute_import
import os

from behave import step
from datetime import datetime
from edutesting.mocks.settings import DT_EXCHANGE_LOG_FILE
from edutesting.mocks.settings import MODE_ALL
from edutesting.mocks.settings import MODE_UPDATE
from edutesting.mocks.settings import RECIPIENT_MNEMONIC
from suds.sudsobject import Object
from waiting import TimeoutExpired
from waiting import wait
from zipfile import ZipFile


@step(u'к РИС отправить запрос DataPush на {mode} данные')
def step_send_datapush_request(context, mode):
    modes = {
        u'все': MODE_ALL,
        u'обновленные': MODE_UPDATE
    }

    mode = modes[mode]
    msg = context.client.factory.create('DataPush')

    service_tag = Object()
    service_tag.__setattr__('Mnemonic', RECIPIENT_MNEMONIC)
    service_tag.__setattr__('Version', '0.01')

    context.session_id = datetime.now().strftime('%y%m%d%H%M%S%f')
    # Message
    msg.Message.Sender.Code = 'CTNG00000'
    msg.Message.Sender.Name = 'CTNG00000'
    msg.Message.Recipient.Code = RECIPIENT_MNEMONIC
    msg.Message.Recipient.Name = RECIPIENT_MNEMONIC
    msg.Message.__setattr__('Service', service_tag)
    msg.Message.TypeCode = 'GSRV'
    msg.Message.Status = 'REQUEST'
    msg.Message.Date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    msg.Message.ExchangeType = '1'

    # MessageData
    msg_data = msg.MessageData.AppData.DataPushRequest
    msg_data.AuthorizationKey = 123
    msg_data.SessionID = context.session_id
    msg_data.Mode = mode
    context.datapush_response = context.client.service.DataPush(
        msg.Message,
        msg.MessageData
    )


@step(u'запрос будет корректно обработан')
def step_check_datapush_response(context):
    msg_data = context.datapush_response.MessageData.AppData.DataPushResult
    assert msg_data.SessionID == context.session_id


@step(u'пакет данных будет отправлен к DataTransfer')
def step_check_packet_in(context):
    context.archive_file_path = ''
    try:
        wait(
            lambda: os.path.exists(DT_EXCHANGE_LOG_FILE),
            timeout_seconds=120
        )
    except TimeoutExpired:
        raise TimeoutExpired(120, "Error in exchange")
    with open(DT_EXCHANGE_LOG_FILE, 'r') as log:
        context.archive_file_path = log.readline()

    assert context.archive_file_path


@step(u'распаковать полученный архив')
def step_unzip_file(context):
    with ZipFile(context.archive_file_path) as zf:
        archive_dir = os.path.dirname(context.archive_file_path)
        file_name = zf.infolist()[0].filename
        file_path = os.path.join(archive_dir, file_name)
        zf.extractall(archive_dir)

    context.acd['xml_file'] = context.XmlParsedObject(file_path)


@step(u'открыть файл с данными')
def step_open_xml_file(context):
    assert 'xml_file' in context.acd
