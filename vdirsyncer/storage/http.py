# -*- coding: utf-8 -*-

from ._rust import RustStorage
from .. import exceptions, native
from ..http import USERAGENT


class HttpStorage(RustStorage):

    storage_name = 'http'
    read_only = True
    _repr_attributes = ('username', 'url')
    _items = None

    # Required for tests.
    _ignore_uids = True

    def __init__(self, url, username='', password='', useragent=USERAGENT,
                 verify_cert=None, auth_cert=None, auth_cert_password=None,
                 **kwargs):
        if kwargs.get('collection') is not None:
            raise exceptions.UserError('HttpStorage does not support '
                                       'collections.')

        super(HttpStorage, self).__init__(**kwargs)

        self._native_storage = native.ffi.gc(
            native.lib.vdirsyncer_init_http(
                url.encode('utf-8'),
                (username or "").encode('utf-8'),
                (password or "").encode('utf-8'),
                (useragent or "").encode('utf-8'),
                (verify_cert or "").encode('utf-8'),
                (auth_cert or "").encode('utf-8'),
                (auth_cert_password or "").encode('utf-8')
            ),
            native.lib.vdirsyncer_storage_free
        )

        self.username = username
        self.url = url
