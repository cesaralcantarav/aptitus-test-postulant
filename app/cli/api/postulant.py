import json
import requests

from cli.utils import constants

def validate_status_code(response):
    if response.status_code == constants.STATUS_CODE_503:
        raise Exception('Status Code: {}'.format(response.status_code))

class PostulantApi(object):

    def __init__(self, base_url):
        self.headers = { 'cache-control': 'no-cache'}
        self.base_url = base_url

    def set_headers(self, headers):
        if headers is not None:
            if not 'cache-control' in sorted(headers):
                headers.update(self.headers)
        self.headers = headers

    def registro_rapido(self, payload):
        url = '{}/registro-rapido-ajax'.format(self.base_url)
        r = requests.post(url, headers=self.headers, data=json.dumps(payload))
        return r

