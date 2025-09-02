"""Python SDK for maib ecommerce API"""

import logging
import json
import hashlib
import hmac
import base64

import httpx

logger = logging.getLogger(__name__)


# Based on PHP SDK for maib ecommerce API https://github.com/maib-ecomm/maib-sdk-php (https://packagist.org/packages/maib-ecomm/maib-sdk-php)
# maib e-commerce API https://docs.maibmerchants.md

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

    _base_url: str = None

    def __init__(self, base_url: str = DEFAULT_BASE_URL):
        self._base_url = base_url

    def _build_url(self, url: str, entity_id: str = None):
        """Build the complete URL for the request"""

        url = self._base_url + url

        if entity_id:
            url = f'{url}/{entity_id}'

        return url

    def _process_response(self, response: httpx.Response):
        if response.is_error:
            logger.error('%s Error: %d %s', MaibSdk.__qualname__, response.status_code, response.text, extra={'method': response.request.method, 'url': response.request.url, 'response_text': response.text, 'status_code': response.status_code})
            #response.raise_for_status()

        response_json: dict = response.json()
        logger.debug('%s Response: %d', MaibSdk.__qualname__, response.status_code, extra={'response_json': response_json})
        return response_json

    def send_request(self, method: str, url: str, data: dict = None, token: str = None, entity_id: str = None):
        """Send a request and parse the response."""

        auth = BearerAuth(token) if token else None
        url = self._build_url(url=url, entity_id=entity_id)

        logger.debug('%s Request: %s %s', MaibSdk.__qualname__, method, url, extra={'method': method, 'url': url, 'data': data, 'token': token})
        with httpx.Client() as client:
            response = client.request(method=method, url=url, json=data, auth=auth, timeout=self.DEFAULT_TIMEOUT)
            return self._process_response(response=response)

    async def send_request_async(self, method: str, url: str, data: dict = None, token: str = None, entity_id: str = None):
        """Send async request and parse the response."""

        auth = BearerAuth(token) if token else None
        url = self._build_url(url=url, entity_id=entity_id)

        logger.debug('%s Request: %s %s', MaibSdk.__qualname__, method, url, extra={'method': method, 'url': url, 'data': data, 'token': token})
        async with httpx.AsyncClient() as client:
            response = await client.request(method=method, url=url, json=data, auth=auth, timeout=self.DEFAULT_TIMEOUT)
            return self._process_response(response=response)

    @staticmethod
    def handle_response(response: dict, endpoint: str):
        """Handles errors returned by the API."""

        if not isinstance(response, dict):
            raise MaibPaymentException(f"Invalid response received from server for endpoint {endpoint}")

        if response.get('ok') is True:
            response_result: dict = response.get('result')
            if response_result is not None:
                return response_result

            raise MaibPaymentException(f'Invalid response received from server for endpoint {endpoint}: missing \'result\' field.')

        response_errors = response.get('errors')
        if isinstance(response_errors, list) and response_errors:
            error: dict = response_errors[0]
            raise MaibPaymentException(f'Error sending request to endpoint {endpoint}: {error.get('errorMessage')} ({error.get('errorCode')})')

        raise MaibPaymentException(f'Invalid response received from server for endpoint {endpoint}: missing \'ok\' and \'errors\' fields')

    @staticmethod
    def validate_callback_signature(callback_data: dict, signature_key: str):
        """Validates the callback data signature."""
        # https://docs.maibmerchants.md/en/notifications-on-callback-url
        # https://github.com/maib-ecomm/maib-sdk-php/blob/main/examples/callbackUrl.php

        if not signature_key:
            raise MaibPaymentException('Invalid signature key')

        callback_signature: str = callback_data.get('signature')
        callback_result: dict[str, any] = callback_data.get('result')

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

#region Auth
class BearerAuth(httpx.Auth):
    """Attaches HTTP Bearer Token Authentication to the given Request object."""
    # https://www.python-httpx.org/advanced/authentication/#custom-authentication-schemes

    token: str = None

    def __init__(self, token: str):
        self.token = token

    def auth_flow(self, request: httpx.Request):
        request.headers['Authorization'] = f'Bearer {self.token}'
        yield request
#endregion

#region Exceptions
class MaibTokenException(Exception):
    pass

class MaibPaymentException(Exception):
    pass
#endregion
