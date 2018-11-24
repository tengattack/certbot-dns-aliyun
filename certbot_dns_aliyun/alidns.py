
from datetime import datetime
from hashlib import sha1
import hmac
import uuid
try:
    # Python 3.x
    from urllib.parse import quote_plus
except:
    # Python 2.x
    from urllib import quote_plus

import requests
from certbot import errors

API_ENDPOINT = 'https://alidns.aliyuncs.com/'

class AliError(Exception):
    def __init__(self, message, code, request_id):
        # Call the base class constructor with the parameters it needs
        super(AliError, self).__init__(message)

        # Aliyun code...
        self.Code = code
        self.RequestId = request_id

class AliDNSClient():
    """
    Encapsulates all communication with the Aliyun DNS Serivce.
    """

    _access_key = ''
    _access_key_secret = ''
    _ttl = 600

    def __init__(self, access_key, access_key_secret, ttl = 600):
        self._access_key = access_key
        self._access_key_secret = access_key_secret
        self._ttl = ttl

    def get_domain_records(self, domain,
                           rr_keyword = '', type_keyword = '', value_keyword = ''):
        return self._request('DescribeDomainRecords', {
            'DomainName': domain,
            'RRKeyWord': rr_keyword,
            'TypeKeyWord': type_keyword,
            'ValueKeyWord': value_keyword,
        })

    def add_txt_record(self, domain, rr, value):
        self._request('AddDomainRecord', {
            'DomainName': domain,
            'RR': rr,
            'Type': 'TXT',
            'Value': value,
            'TTL': self._ttl,
        })

    def del_txt_record(self, domain, rr, value):
        records = self.get_domain_records(domain, rr_keyword=rr, type_keyword='TXT')
        record_id = ''
        for record in records['DomainRecords']['Record']:
            if record['RR'] == rr:
                record_id = record['RecordId']
                break
        if record_id:
            self._request('DeleteDomainRecord', {
                'DomainName': domain,
                'RecordId': record_id,
            })

    def _urlencode(self, s):
        s = quote_plus(s)
        return s.replace('+', '%20').replace('%7E', '~')

    def _request(self, action, data):
        timestamp = datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
        params = {
            'Format': 'JSON',
            'Version': '2015-01-09',
            'AccessKeyId': self._access_key,
            'SignatureMethod': 'HMAC-SHA1',
            'Timestamp': timestamp,
            'SignatureVersion': '1.0',
            'SignatureNonce': str(uuid.uuid4()),
            'Action': action,
        }
        params.update(data)

        str_to_sign = ''
        for key in sorted(params.iterkeys()):
            str_to_sign += '&' + self._urlencode(key) + '=' + self._urlencode(str(params[key]))
        # remove the first &
        str_to_sign = 'GET&%2F&' + self._urlencode(str_to_sign[1:])

        h = hmac.new(self._access_key_secret + '&', str_to_sign, sha1)
        params['Signature'] = h.digest().encode("base64").rstrip('\n')

        r = requests.get(API_ENDPOINT, params=params)
        r = r.json()

        if 'Code' in r:
            e = AliError(r['Message'], r['Code'], r['RequestId'])
            if 'DomainName' in data:
                result = self._handle_general_error(e, data['DomainName'])
                if result:
                    raise result
            raise e

        return r

    def _handle_general_error(self, e, domain_name):
        if e.Code.startswith('InvalidAccessKeyId.'):
            hint = 'Are your AccessKey and AccessKeySecret values correct?'
            return errors.PluginError('Error determining zone identifier for {0}: {1}{2}'
                                      .format(domain_name, e, ' ({0})'.format(hint) if hint else ''))
        if not e.Code.startswith('InvalidDomainName.'):
            return errors.PluginError('Unexpected error determining zone identifier for {0}: {1}'
                                      .format(domain_name, e))
