import json
import logging
import hashlib
import base64

import requests

#This module is based on PHP SDK for maib ecommerce API https://github.com/maib-ecomm/maib-sdk-php

class MAIBSDK:
    # maib ecommerce API base url
    DEFAULT_BASE_URL = 'https://api.maibmerchants.md/v1/'

    # maib ecommerce API endpoints
    GET_TOKEN = 'generate-token'
    DIRECT_PAY = 'pay'
    HOLD = 'hold'
    COMPLETE = 'complete'
    REFUND = 'refund'
    PAY_INFO = 'pay-info'
    SAVE_REC = 'savecard-recurring'
    EXE_REC = 'execute-recurring'
    SAVE_ONECLICK = 'savecard-oneclick'
    EXE_ONECLICK = 'execute-oneclick'
    DELETE_CARD = 'delete-card'

    DEFAULT_TIMEOUT = 30

    _instance = None
    base_url: str = None

    def __init__(self):
        self.base_url = MAIBSDK.DEFAULT_BASE_URL

    @staticmethod
    def get_instance():
        if MAIBSDK._instance is None:
            MAIBSDK._instance = MAIBSDK()

        return MAIBSDK._instance

    def build_url(self, url: str, entity_id: str = None):
        url = self.base_url + url

        if entity_id:
            url = f'{url}/{entity_id}'

        return url

    def send_request(self, method: str, url: str, data: dict = None, token: str = None, entity_id: str = None):
        auth = BearerAuth(token) if token else None

        url = self.build_url(url=url, entity_id=entity_id)
        logging.debug('MAIBSDK REQUEST', extra={'method': method, 'url': url, 'data': data})
        with requests.request(method=method, url=url, json=data, auth=auth, timeout=MAIBSDK.DEFAULT_TIMEOUT) as response:
            response_json = response.json()
            logging.debug('MAIBSDK RESPONSE', extra={'response_json': response_json})
            #response.raise_for_status()
            return response_json

    def handle_response(self, response: dict, endpoint: str):
        response_ok = response.get('ok')
        if response_ok is not None and response_ok is True:
            response_result = response.get('result')
            if response_result is not None:
                return response_result

            raise MAIBPaymentException(f'Invalid response received from server for endpoint {endpoint}: missing \'result\' field.')

        response_errors = response.get('errors')
        if response_errors is not None:
            error = response_errors[0]
            raise MAIBPaymentException(f'Error sending request to endpoint $endpoint: {error.get('errorMessage')} ({error.get('errorCode')})')

        raise MAIBPaymentException(f'Invalid response received from server for endpoint {endpoint}: missing \'ok\' and \'errors\' fields')

    @staticmethod
    def validate_callback_signature(callback_data: dict, signature_key: str):
        #https://docs.maibmerchants.md/ro/notificari-pe-callback-url
        #https://github.com/maib-ecomm/maib-sdk-php/blob/main/examples/callbackUrl.php
        callback_signature = callback_data.get('signature')
        if not callback_signature:
            raise MAIBPaymentException('Missing callback signature')

        callback_result = callback_data['result']
        sorted_callback_result = {key: str(value) for key, value in sorted(callback_result.items())}
        sorted_callback_values = list(sorted_callback_result.values())
        sorted_callback_values.append(signature_key)

        sign_string = ':'.join(sorted_callback_values)
        calculated_signature = base64.b64encode(hashlib.sha256(sign_string.encode()).digest()).decode()

        return calculated_signature == callback_signature

    @staticmethod
    def get_error_message(response: str):
        error_message = ''

        if response:
            response_obj = json.loads(response)

            #https://stackoverflow.com/questions/363944/python-idiom-to-return-first-item-or-none
            response_error = next(iter(response_obj.get('errors', [])), None)
            if response_error:
                error_message = response_error.get('errorMessage')
            else:
                error_message = 'Unknown error details.'

        return error_message

#region Requests
#https://stackoverflow.com/questions/29931671/making-an-api-call-in-python-with-an-api-that-requires-a-bearer-token
#https://requests.readthedocs.io/en/latest/user/authentication/#new-forms-of-authentication
class BearerAuth(requests.auth.AuthBase):
    token: str = None

    def __init__(self, token: str):
        self.token = token

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        request.headers["Authorization"] = f'Bearer {self.token}'
        return request
#endregion

#region Exceptions
class MAIBTokenException(Exception):
    pass

class MAIBPaymentException(Exception):
    pass
#endregion
