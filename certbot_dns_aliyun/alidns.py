
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
from certbot.plugins import dns_common

API_ENDPOINT = 'https://alidns.aliyuncs.com/'

class AliError(Exception):
    def __init__(self, message, code, request_id):
        # Call the base class constructor with the parameters it needs
        super(AliError, self).__init__(message.rstrip('.'))

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

    def _find_domain_id(self, domain):
        domain_name_guesses = dns_common.base_domain_name_guesses(domain)

        for domain_name in domain_name_guesses:
            r = self._request('DescribeDomains', {
                'KeyWord': domain_name,
            })
            for d in r['Domains']['Domain']:
                if d['DomainName'] == domain_name:
                    return domain_name

        raise errors.PluginError('Unable to determine zone identifier for {0} using zone names: {1}'
                                 .format(domain, domain_name_guesses))

    def _find_domain_record_id(self, domain, rr = '', typ = '', value = ''):
        records = self._request('DescribeDomainRecords', {
            'DomainName': domain,
            'RRKeyWord': rr,
            'TypeKeyWord': typ,
            'ValueKeyWord': value,
        })
        for record in records['DomainRecords']['Record']:
            if record['RR'] == rr:
                return record['RecordId']
        raise errors.PluginError('Unexpected error determining record identifier for {0}: {1}'
                                 .format(rr, 'record not found'))

    def add_txt_record(self, domain, record_name, value):
        domain = self._find_domain_id(domain)
        rr = record_name[:record_name.rindex('.' + domain)]
        self._request('AddDomainRecord', {
            'DomainName': domain,
            'RR': rr,
            'Type': 'TXT',
            'Value': value,
            'TTL': self._ttl,
        })

    def del_txt_record(self, domain, record_name, value):
        domain = self._find_domain_id(domain)
        rr = record_name[:record_name.rindex('.' + domain)]
        record_id = self._find_domain_record_id(domain, rr=rr, typ='TXT')
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
