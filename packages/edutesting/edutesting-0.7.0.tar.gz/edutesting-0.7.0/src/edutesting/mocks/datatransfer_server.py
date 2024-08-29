# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function
import datetime
import os
import sys

from datatransfer.common import constants
from datatransfer.common.smev256 import Smev256 as huge_smev
from datatransfer.source.configs import DATATRANSFER_MNEMONICS
from pem import parse_file
from spyne.decorator import rpc
from spyne.error import Fault
from spyne.model import ComplexModel
from spyne.service import ServiceBase
from spyne.model.primitive import Unicode
from spyne_smev.application import Application
from spyne_smev.server.wsgi import WsgiApplication
from spyne_smev.wsse.protocols import X509TokenProfile
from wsgiref.simple_server import make_server

from .settings import CERT_PATH
from .settings import CURRENT_CONFIG_PATH
from .settings import DT_EXCHANGE_LOG_FILE
from .settings import RECIPIENT_MNEMONIC


class ComplexModelWithNamespace(ComplexModel):
    __namespace__ = 'http://bars-open.ru/inf'


class DataTransferRequest(ComplexModelWithNamespace):
    AuthorizationKey = Unicode
    SessionID = Unicode


class DataTransferResponse(ComplexModel):
    __namespace__ = 'http://bars-open.ru/inf' + '/response'
    SessionID = Unicode
    Message = Unicode


class DataTransferService(ServiceBase):

    @rpc(DataTransferRequest, _returns=DataTransferResponse)
    def DataTransfer(context, DataTransferRequest):
        now = datetime.datetime.now()

        InMessage = context.udc.in_smev_message
        OutMessage = context.udc.out_smev_message

        response = DataTransferResponse()
        response.SessionID = DataTransferRequest.SessionID

        AppDocument = context.udc.in_smev_appdoc
        dt_log_file = open(DT_EXCHANGE_LOG_FILE, 'w')
        try:
            today = datetime.date.today()

            archive_path = os.path.join(
                CURRENT_CONFIG_PATH, 'log',
                constants.CONFIGURATION_ARCHIVE_IN,
                str(today.year), str(today.month), str(today.day))

            archive_filename = os.path.join(
                archive_path,
                u"{0}_{1}_{2}.zip".format(
                    InMessage.Sender.Code, AppDocument.RequestCode,
                    now.strftime('%Y%m%d_%H%M%S')))

            try:
                if not os.path.exists(archive_path):
                    os.makedirs(archive_path)

                with open(archive_filename, 'w+b') as decoded_file:
                    decoded_file.write(
                        AppDocument.BinaryData.data.pop())

                dt_log_file.write(archive_filename)

            except Exception as e:
                dt_log_file.write('Access error')
                raise Fault(
                    faultcode=u"FAILURE",
                    faultstring=u"Ошибка доступа к файлу: {0}".format(str(e))
                )

        except Fault as e:
            OutMessage.Status = e.faultcode
            response.Message = e.faultstring
            dt_log_file.write('Build error')

        dt_log_file.close()
        return response


CERT, PRIV_KEY = parse_file(CERT_PATH)
OUT_SEC = X509TokenProfile(
   private_key=str(PRIV_KEY),
   private_key_pass='1234567890',
   certificate=str(CERT),
   digest_method="md_gost94",
)


IN_PROTOCOL = huge_smev()
OUT_PROTOCOL = huge_smev(
    wsse_security=OUT_SEC,
    SenderCode=DATATRANSFER_MNEMONICS,
    SenderName=DATATRANSFER_MNEMONICS,
    RecipientCode=RECIPIENT_MNEMONIC,
    RecipientName=RECIPIENT_MNEMONIC,
    Mnemonic=DATATRANSFER_MNEMONICS,
    Version="1.00")


def main():
    application = Application(
        [DataTransferService], 'http://bars-open.ru/inf',
        in_protocol=IN_PROTOCOL,
        out_protocol=OUT_PROTOCOL
    )

    try:
        port = int(sys.argv[1])
    except IndexError:
        raise IndexError(
            'Set port for datatransfer. '
            'Use command: datatransfer <port_number>'
        )

    try:
        import logging
        logging.basicConfig(level=logging.DEBUG)
        wsgi_application = WsgiApplication(application)
        server = make_server("localhost", port, wsgi_application)
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nGoodbye!')
