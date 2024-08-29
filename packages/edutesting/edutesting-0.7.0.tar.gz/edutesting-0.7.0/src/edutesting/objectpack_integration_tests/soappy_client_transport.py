# -*- coding: utf-8 -*-
"""
Transport для SOAPpy, запросы отправляются через
Django.test.client/Client
"""
from __future__ import absolute_import
from __future__ import unicode_literals

import re
from SOAPpy import Config
from SOAPpy import SOAPAddress
from SOAPpy import StringType
from SOAPpy import HTTPError
from SOAPpy import Cookie

from django.test.client import Client


class DjangoHTTPTransport(object):
    """
    Transport для SOAPpy, запросы отправляются через
    Django.test.client/Client
    """
    def __init__(self):
        """
        Инициализация созданного объекта
        """
        self.cookies = Cookie.SimpleCookie()

        self.c = Client()

    def getNS(self, original_namespace, data):
        """
        Extract the (possibly extended) namespace from the returned
        SOAP message."""

        if type(original_namespace) == StringType:
            pattern = "xmlns:\w+=['\"](" + original_namespace + "[^'\"]*)['\"]"
            match = re.search(pattern, data)
            if match:
                return match.group(1)
            else:
                return original_namespace
        else:
            return original_namespace

    def __addcookies(self, r):
        """
        Add cookies from self.cookies to request r
        """
        for cname, morsel in self.cookies.items():
            attrs = []
            value = morsel.get('version', '')
            if value != '' and value != '0':
                attrs.append('$Version=%s' % value)
            attrs.append('%s=%s' % (cname, morsel.coded_value))
            value = morsel.get('path')
            if value:
                attrs.append('$Path=%s' % value)
            value = morsel.get('domain')
            if value:
                attrs.append('$Domain=%s' % value)
            r.putheader('Cookie', "; ".join(attrs))

    def call(
            self, addr, data, namespace, soapaction=None, encoding=None,
            http_proxy=None, config=Config, timeout=None
    ):

        if not isinstance(addr, SOAPAddress):
            addr = SOAPAddress(addr, config)

        r = {}
        t = 'text/xml'
        if encoding is not None:
            t += '; charset=%s' % encoding
        r.update({"Content-type": t})
        r.update({"Content-length": str(len(data))})

        # This fixes sending either "" or "None"
        if soapaction is None or len(soapaction) == 0:
            r.update({"HTTP_SOAPACTION": ""})
        else:
            r.update({"HTTP_SOAPACTION": '"%s"' % soapaction})

        # r.endheaders()

        # send the payload
        response = self.c.post(
            addr.path,
            data=data,
            content_type="text/xml",
            **r
        )

        headers = {}
        for i in response._headers.values():
            headers.update(dict([i]))

        code = response.status_code

        data = response.content
        message_len = len(data)

        def startswith(string, val):
            return string[0:len(val)] == val

        if (code == 500 and not
                (startswith(data, "text/xml") and message_len > 0)):
            raise HTTPError(code, data)

        if code not in (200, 500):
            raise HTTPError(code, data)

        # get the new namespace
        if namespace is None:
            new_ns = None
        else:
            new_ns = self.getNS(namespace, data)

        # return response payload
        return data, new_ns
