"""Python SDK for maib ecommerce API"""

import json
import logging
import hashlib
import hmac
import base64

import requests

# Based on PHP SDK for maib ecommerce API https://github.com/maib-ecomm/maib-sdk-php (https://packagist.org/packages/maib-ecomm/maib-sdk-php)

logger = logging.getLogger(__name__)

class MaibSdk:
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

    __instance = None
    __base_url: str = None

    def __init__(self):
        self.__base_url = MaibSdk.DEFAULT_BASE_URL

    @staticmethod
    def get_instance():
        """Get the instance of MaibSdk (Singleton pattern)"""

        if MaibSdk.__instance is None:
            MaibSdk.__instance = MaibSdk()

        return MaibSdk.__instance

    def __build_url(self, url: str, entity_id: str = None):
        """Build the complete URL for the request"""

        url = self.__base_url + url

        if entity_id:
            url = f'{url}/{entity_id}'

        return url

    def send_request(self, method: str, url: str, data: dict = None, token: str = None, entity_id: str = None):
        """Send a request and parse the response."""

        auth = BearerAuth(token) if token else None
        url = self.__build_url(url=url, entity_id=entity_id)

        logger.debug('MaibSdk Request', extra={'method': method, 'url': url, 'data': data, 'token': token})
        with requests.request(method=method, url=url, json=data, auth=auth, timeout=MaibSdk.DEFAULT_TIMEOUT) as response:
            if not response.ok:
                logger.error('MaibSdk Error', extra={'method': method, 'url': url, 'response_text': response.text, 'status_code': response.status_code})
                #response.raise_for_status()
                return None

            response_json: dict = response.json()
            logger.debug('MaibSdk Response', extra={'response_json': response_json})
            return response_json

    @staticmethod
    def handle_response(response: dict, endpoint: str):
        """Handles errors returned by the API."""

        response_ok = response.get('ok')
        if response_ok is not None and response_ok is True:
            response_result: dict = response.get('result')
            if response_result is not None:
                return response_result

            raise MaibPaymentException(f'Invalid response received from server for endpoint {endpoint}: missing \'result\' field.')

        response_errors = response.get('errors')
        if response_errors is not None:
            error = response_errors[0]
            raise MaibPaymentException(f'Error sending request to endpoint {endpoint}: {error.get('errorMessage')} ({error.get('errorCode')})')

        raise MaibPaymentException(f'Invalid response received from server for endpoint {endpoint}: missing \'ok\' and \'errors\' fields')

    @staticmethod
    def validate_callback_signature(callback_data: dict, signature_key: str):
        """Validates the callback data signature."""
        #https://docs.maibmerchants.md/en/notifications-on-callback-url
        #https://github.com/maib-ecomm/maib-sdk-php/blob/main/examples/callbackUrl.php

        if not signature_key:
            raise MaibPaymentException('Invalid signature key')

        callback_signature = callback_data.get('signature')
        callback_result = callback_data.get('result')

        if not callback_signature or not callback_result:
            raise MaibPaymentException('Missing result or signature in callback data.')

        sorted_callback_result = {key: (str(value) if value is not None else '') for key, value in sorted(callback_result.items())}
        sorted_callback_values = list(sorted_callback_result.values())
        sorted_callback_values.append(signature_key)

        sign_string = ':'.join(sorted_callback_values)
        calculated_signature = base64.b64encode(hashlib.sha256(sign_string.encode()).digest()).decode()

        return hmac.compare_digest(calculated_signature, callback_signature)

    @staticmethod
    def get_error_message(response: str):
        """Retrieves the error message from the API response."""

        error_message = ''
        if response:
            response_obj = json.loads(response)

            response_error = next(iter(response_obj.get('errors', [])), None)
            if response_error:
                error_message = response_error.get('errorMessage')
            else:
                error_message = 'Unknown error details.'

        return error_message

#region Requests
class BearerAuth(requests.auth.AuthBase):
    """Attaches HTTP Bearer Token Authentication to the given Request object."""
    #https://requests.readthedocs.io/en/latest/user/authentication/#new-forms-of-authentication

    token: str = None

    def __init__(self, token: str):
        self.token = token

    def __call__(self, request: requests.PreparedRequest):
        request.headers["Authorization"] = f'Bearer {self.token}'
        return request
#endregion

#region Exceptions
class MaibTokenException(Exception):
    pass

class MaibPaymentException(Exception):
    pass
#endregion
