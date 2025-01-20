import logging
from .maibsdk import MAIBSDK, MAIBPaymentException

class MAIBAPIRequest:
    @staticmethod
    def create():
        client = MAIBSDK()
        return MAIBAPI(client)

class MAIBAPI:
    client: MAIBSDK = None
    REQUIRED_PAY_PARAMS = ['amount', 'currency', 'clientIp']
    REQUIRED_PAYID_PARAMS = ['payId']
    REQUIRED_SAVE_PARAMS = ['billerExpiry', 'currency', 'clientIp']
    REQUIRED_EXECUTE_RECURRING_PARAMS = ['billerId', 'amount', 'currency']
    REQUIRED_EXECUTE_ONECLICK_PARAMS = ['billerId', 'amount', 'currency', 'clientIp']

    def __init__(self, client: MAIBSDK):
        self.client = client

    def pay(self, data: dict, token: str):
        return self.execute_pay_operation(endpoint=MAIBSDK.DIRECT_PAY, data=data, token=token, required_params=MAIBAPI.REQUIRED_PAY_PARAMS)

    def hold(self, data: dict, token: str):
        return self.execute_pay_operation(endpoint=MAIBSDK.HOLD, data=data, token=token, required_params=MAIBAPI.REQUIRED_PAY_PARAMS)

    def complete(self, data: dict, token: str):
        return self.execute_pay_operation(endpoint=MAIBSDK.COMPLETE, data=data, token=token, required_params=MAIBAPI.REQUIRED_PAYID_PARAMS)

    def refund(self, data: dict, token: str):
        return self.execute_pay_operation(endpoint=MAIBSDK.REFUND, data=data, token=token, required_params=MAIBAPI.REQUIRED_PAYID_PARAMS)

    def pay_info(self, pay_id: str, token: str):
        return self.execute_entity_id_operation(endpoint=MAIBSDK.PAY_INFO, entity_id=pay_id, token=token)

    def delete_card(self, entity_id: str, token: str):
        return self.execute_entity_id_operation(method='DELETE', endpoint=MAIBSDK.DELETE_CARD, entity_id=entity_id, token=token)

    def save_recurring(self, data: dict, token: str):
        return self.execute_pay_operation(endpoint=MAIBSDK.SAVE_REC, data=data, token=token, required_params=MAIBAPI.REQUIRED_SAVE_PARAMS)

    def execute_recurring(self, data: dict, token: str):
        return self.execute_pay_operation(endpoint=MAIBSDK.EXE_REC, data=data, token=token, required_params=MAIBAPI.REQUIRED_EXECUTE_RECURRING_PARAMS)

    def save_oneclick(self, data: dict, token: str):
        return self.execute_pay_operation(endpoint=MAIBSDK.SAVE_ONECLICK, data=data, token=token, required_params=MAIBAPI.REQUIRED_SAVE_PARAMS)

    def execute_oneclick(self, data: dict, token: str):
        return self.execute_pay_operation(endpoint=MAIBSDK.EXE_ONECLICK, data=data, token=token, required_params=MAIBAPI.REQUIRED_EXECUTE_ONECLICK_PARAMS)

    def execute_pay_operation(self, endpoint: str, data: dict, token: str, required_params: list, method: str = 'POST'):
        try:
            self.validate_pay_params(data=data, required_params=required_params)
            self.validate_access_token(token=token)
            return self.send_request(method=method, endpoint=endpoint, data=data, token=token)
        except MAIBPaymentException as ex:
            logging.exception('MAIBAPI.execute_pay_operation')
            raise MAIBPaymentException(f'Invalid request: {ex}') from ex

    def execute_entity_id_operation(self, endpoint: str, entity_id: str, token: str, method: str = 'GET'):
        try:
            self.validate_id_param(entity_id=entity_id)
            self.validate_access_token(token=token)
            return self.send_request(method=method, endpoint=endpoint, token=token, entity_id=entity_id)
        except MAIBPaymentException as ex:
            logging.exception('MAIBAPI.execute_entity_id_operation')
            raise MAIBPaymentException(f'Invalid request: {ex}') from ex

    def send_request(self, method: str, endpoint: str, token: str, data: dict = None, entity_id: str = None):
        try:
            response = self.client.send_request(method=method, url=endpoint, data=data, token=token, entity_id=entity_id)
        except Exception as ex:
            raise MAIBPaymentException(f'HTTP error while sending {method} request to endpoint {endpoint}: {ex}') from ex

        return self.client.handle_response(response, endpoint)

    def validate_access_token(self, token: str):
        if not token or len(token) == 0:
            raise MAIBPaymentException('Access token is not valid. It should be a non-empty string.')

    def validate_id_param(self, entity_id: str):
        if not entity_id:
            raise MAIBPaymentException('Missing ID.')

        if len(entity_id) == 0:
            raise MAIBPaymentException('Invalid ID parameter. Should be string of 36 characters.')

    def validate_pay_params(self, data: dict, required_params: list):
        # Check that all required parameters are present
        for param in required_params:
            if data.get(param) is None:
                raise MAIBPaymentException(f'Missing required parameter: {param}')

        # Check that parameters have the expected types and formats
        biller_id = data.get('billerId')
        if biller_id is not None:
            if not isinstance(biller_id, str) or len(biller_id) != 36:
                raise MAIBPaymentException('Invalid \'billerId\' parameter. Should be a string of 36 characters.')

        biller_expiry = data.get('billerExpiry')
        if biller_expiry is not None:
            if not isinstance(biller_expiry, str) or len(biller_expiry) != 4:
                raise MAIBPaymentException('Invalid \'billerExpiry\' parameter. Should be a string of 4 characters.')

        pay_id = data.get('payId')
        if pay_id is not None:
            if not isinstance(pay_id, str) or len(pay_id) > 36:
                raise MAIBPaymentException('Invalid \'payId\' parameter. Should be a string of 36 characters.')

        confirm_amount = data.get('confirmAmount')
        if confirm_amount is not None:
            if not isinstance(confirm_amount, (float, int)) or confirm_amount < 0.01:
                raise MAIBPaymentException('Invalid \'confirmAmount\' parameter. Should be a numeric value > 0.')

        amount = data.get('amount')
        if amount is not None:
            if not isinstance(amount, (float, int)) or amount < 1:
                raise MAIBPaymentException('Invalid \'amount\' parameter. Should be a numeric value >= 1.')

        refund_amount = data.get('refundAmount')
        if refund_amount is not None:
            if not isinstance(refund_amount, (float, int)) or refund_amount < 0.01:
                raise MAIBPaymentException('Invalid \'refundAmount\' parameter. Should be a numeric value > 0.')

        currency = data.get('currency')
        if currency is not None:
            if not isinstance(currency, str) or currency not in ['MDL', 'EUR', 'USD']:
                raise MAIBPaymentException('Invalid \'currency\' parameter. Currency should be one of \'MDL\', \'EUR\', or \'USD\'.')

        client_ip = data.get('clientIp')
        if client_ip is not None:
            #TODO: Validate IP address
            if not isinstance(client_ip, str):
                raise MAIBPaymentException('Invalid \'clientIp\' parameter. Please provide a valid IP address.')

        language = data.get('language')
        if language is not None:
            if not isinstance(language, str) or len(language) != 2:
                raise MAIBPaymentException('Invalid \'language\' parameter. Should be a string of 2 characters.')

        description = data.get('description')
        if description is not None:
            if not isinstance(description, str) or len(description) > 124:
                raise MAIBPaymentException('Invalid \'description\' parameter. Should be a string and not exceed 124 characters.')

        client_name = data.get('clientName')
        if client_name is not None:
            if not isinstance(client_name, str) or len(client_name) > 128:
                raise MAIBPaymentException('Invalid \'clientName\' parameter. Should be a string and not exceed 128 characters.')

        email = data.get('email')
        if email is not None:
            #TODO: Validate email address
            if not isinstance(email, str):
                raise MAIBPaymentException('Invalid \'email\' parameter. Please provide a valid email address.')

        phone = data.get('phone')
        if phone is not None:
            if not isinstance(phone, str) or len(phone) > 40:
                raise MAIBPaymentException('Invalid \'phone\' parameter. Phone number should not exceed 40 characters.')

        order_id = data.get('orderId')
        if order_id is not None:
            if not isinstance(order_id, str) or len(order_id) > 36:
                raise MAIBPaymentException('Invalid \'orderId\' parameter. Should be a string and not exceed 36 characters.')

        delivery = data.get('delivery')
        if delivery is not None:
            if not isinstance(delivery, (float, int)) or delivery < 0:
                raise MAIBPaymentException('Invalid \'delivery\' parameter. Delivery fee should be a numeric value >= 0.')

        items = data.get('items')
        if items is not None:
            if not isinstance(items, list) or len(items) == 0:
                raise MAIBPaymentException('Invalid \'items\' parameter. Items should be a non-empty list.')

            for item in items:
                item_id = item.get('id')
                if item_id is not None:
                    if not isinstance(item_id, str) or len(item_id) > 36:
                        raise MAIBPaymentException('Invalid \'id\' parameter in the \'items\' list. Should be a string and not exceed 36 characters.')

                item_name = item.get('name')
                if item_name is not None:
                    if not isinstance(item_name, str) or len(item_name) > 128:
                        raise MAIBPaymentException('Invalid \'name\' parameter in the \'items\' list. Should be a string and not exceed 128 characters.')

                item_price = item.get('price')
                if item_price is not None:
                    if not isinstance(item_price, (float, int)) or item_price < 0:
                        raise MAIBPaymentException('Invalid \'price\' parameter in the \'items\' list. Item price should be a numeric value >= 0.')

                quantity = item.get('quantity')
                if quantity is not None:
                    if not isinstance(quantity, int) or quantity < 0:
                        raise MAIBPaymentException('Invalid \'quantity\' parameter in the \'items\' array. Item quantity should be a numeric value >= 0.')

        callback_url = data.get('callbackUrl')
        if callback_url is not None:
            #TODO: Validate URL
            if not isinstance(callback_url, str):
                raise MAIBPaymentException('Invalid \'callbackUrl\' parameter. Should be a string url.')

        ok_url = data.get('okUrl')
        if ok_url is not None:
            #TODO: Validate URL
            if not isinstance(ok_url, str):
                raise MAIBPaymentException('Invalid \'ok_url\' parameter. Should be a string url.')

        fail_url = data.get('failUrl')
        if fail_url is not None:
            #TODO: Validate URL
            if not isinstance(fail_url, str):
                raise MAIBPaymentException('Invalid \'fail_url\' parameter. Should be a string url.')

        return True
