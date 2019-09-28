"""Tests for certbot_dns_aliyun.alidns."""

import os
import unittest

try:
    from .alidns import AliDNSClient
except:
    from alidns import AliDNSClient

ACCESS_KEY = '123'
ACCESS_KEY_SECRET = 'bar'
DOMAIN_NAME = 'foo.bar.example.com'

class AliDNSClientTest(unittest.TestCase):

    _client = None

    def setUp(self):
        super(AliDNSClientTest, self).setUp()
        self._client = AliDNSClient(ACCESS_KEY, ACCESS_KEY_SECRET)

    def test_add_txt_record(self):
        self._client.add_txt_record(DOMAIN_NAME, 'test.' + DOMAIN_NAME, 'test')

    def test_del_txt_record(self):
        self._client.del_txt_record(DOMAIN_NAME, 'test.' + DOMAIN_NAME, 'test')

if __name__ == "__main__":
    unittest.main()  # pragma: no cover
