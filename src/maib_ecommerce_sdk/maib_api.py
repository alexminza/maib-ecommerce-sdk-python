"""Python SDK for maib ecommerce API"""

from .maib_sdk import MaibSdk, MaibPaymentException


class MaibApiRequest:
    """Factory class responsible for creating new instances of the MaibApi class."""

    @staticmethod
    def create():
        """Creates a new instance of MaibApi."""

        client = MaibSdk()
        return MaibApi(client)

class MaibApi:
    _client: MaibSdk = None

    REQUIRED_PAY_PARAMS = ['amount', 'currency', 'clientIp']
    REQUIRED_PAYID_PARAMS = ['payId']
    REQUIRED_SAVE_PARAMS = ['billerExpiry', 'currency', 'clientIp']
    REQUIRED_EXECUTE_RECURRING_PARAMS = ['billerId', 'amount', 'currency']
    REQUIRED_EXECUTE_ONECLICK_PARAMS = ['billerId', 'amount', 'currency', 'clientIp']

    def __init__(self, client: MaibSdk):
        self._client = client

    #region Direct payment
    def pay(self, data: dict, token: str):
        """Direct payment

        https://docs.maibmerchants.md/en/direct-payment"""

        return self._execute_pay_operation(endpoint=MaibSdk.DIRECT_PAY, data=data, token=token, required_params=MaibApi.REQUIRED_PAY_PARAMS)

    async def pay_async(self, data: dict, token: str):
        """Direct payment

        https://docs.maibmerchants.md/en/direct-payment"""

        return await self._execute_pay_operation_async(endpoint=MaibSdk.DIRECT_PAY, data=data, token=token, required_params=MaibApi.REQUIRED_PAY_PARAMS)
    #endregion

    #region Two-step payment
    def hold(self, data: dict, token: str):
        """Payment authorization

        https://docs.maibmerchants.md/en/two-step-payment/payment-authorization"""

        return self._execute_pay_operation(endpoint=MaibSdk.HOLD, data=data, token=token, required_params=MaibApi.REQUIRED_PAY_PARAMS)

    async def hold_async(self, data: dict, token: str):
        """Payment authorization

        https://docs.maibmerchants.md/en/two-step-payment/payment-authorization"""

        return await self._execute_pay_operation_async(endpoint=MaibSdk.HOLD, data=data, token=token, required_params=MaibApi.REQUIRED_PAY_PARAMS)

    def complete(self, data: dict, token: str):
        """Payment capture

        https://docs.maibmerchants.md/en/two-step-payment/payment-capture"""

        return self._execute_pay_operation(endpoint=MaibSdk.COMPLETE, data=data, token=token, required_params=MaibApi.REQUIRED_PAYID_PARAMS)

    async def complete_async(self, data: dict, token: str):
        """Payment capture

        https://docs.maibmerchants.md/en/two-step-payment/payment-capture"""

        return await self._execute_pay_operation_async(endpoint=MaibSdk.COMPLETE, data=data, token=token, required_params=MaibApi.REQUIRED_PAYID_PARAMS)
    #endregion

    #region Payment refund
    def refund(self, data: dict, token: str):
        """Payment refund

        https://docs.maibmerchants.md/en/payment-refund"""

        return self._execute_pay_operation(endpoint=MaibSdk.REFUND, data=data, token=token, required_params=MaibApi.REQUIRED_PAYID_PARAMS)

    async def refund_async(self, data: dict, token: str):
        """Payment refund

        https://docs.maibmerchants.md/en/payment-refund"""

        return await self._execute_pay_operation_async(endpoint=MaibSdk.REFUND, data=data, token=token, required_params=MaibApi.REQUIRED_PAYID_PARAMS)
    #endregion

    #region Payment information
    def pay_info(self, pay_id: str, token: str):
        """Payment information

        https://docs.maibmerchants.md/en/payment-information"""

        return self._execute_entity_id_operation(endpoint=MaibSdk.PAY_INFO, entity_id=pay_id, token=token)

    async def pay_info_async(self, pay_id: str, token: str):
        """Payment information

        https://docs.maibmerchants.md/en/payment-information"""

        return await self._execute_entity_id_operation_async(endpoint=MaibSdk.PAY_INFO, entity_id=pay_id, token=token)
    #endregion

    #region Recurring payments
    def save_recurring(self, data: dict, token: str):
        """Register card in the maib ecomm system

        https://docs.maibmerchants.md/en/recurring-payments/register-card-in-the-maib-ecomm-system"""

        return self._execute_pay_operation(endpoint=MaibSdk.SAVE_REC, data=data, token=token, required_params=MaibApi.REQUIRED_SAVE_PARAMS)

    async def save_recurring_async(self, data: dict, token: str):
        """Register card in the maib ecomm system

        https://docs.maibmerchants.md/en/recurring-payments/register-card-in-the-maib-ecomm-system"""

        return await self._execute_pay_operation_async(endpoint=MaibSdk.SAVE_REC, data=data, token=token, required_params=MaibApi.REQUIRED_SAVE_PARAMS)

    def execute_recurring(self, data: dict, token: str):
        """Execute recurring payment

        https://docs.maibmerchants.md/en/recurring-payments/execute-recurring-payment"""

        return self._execute_pay_operation(endpoint=MaibSdk.EXE_REC, data=data, token=token, required_params=MaibApi.REQUIRED_EXECUTE_RECURRING_PARAMS)

    async def execute_recurring_async(self, data: dict, token: str):
        """Execute recurring payment

        https://docs.maibmerchants.md/en/recurring-payments/execute-recurring-payment"""

        return await self._execute_pay_operation_async(endpoint=MaibSdk.EXE_REC, data=data, token=token, required_params=MaibApi.REQUIRED_EXECUTE_RECURRING_PARAMS)
    #endregion

    #region One-click payments
    def save_oneclick(self, data: dict, token: str):
        """Register card in the maib ecomm system

        https://docs.maibmerchants.md/en/one-click-payments/register-card-in-the-maib-ecomm-system"""

        return self._execute_pay_operation(endpoint=MaibSdk.SAVE_ONECLICK, data=data, token=token, required_params=MaibApi.REQUIRED_SAVE_PARAMS)

    async def save_oneclick_async(self, data: dict, token: str):
        """Register card in the maib ecomm system

        https://docs.maibmerchants.md/en/one-click-payments/register-card-in-the-maib-ecomm-system"""

        return await self._execute_pay_operation_async(endpoint=MaibSdk.SAVE_ONECLICK, data=data, token=token, required_params=MaibApi.REQUIRED_SAVE_PARAMS)

    def execute_oneclick(self, data: dict, token: str):
        """Execute one-click payment

        https://docs.maibmerchants.md/en/one-click-payments/execute-one-click-payment"""

        return self._execute_pay_operation(endpoint=MaibSdk.EXE_ONECLICK, data=data, token=token, required_params=MaibApi.REQUIRED_EXECUTE_ONECLICK_PARAMS)

    async def execute_oneclick_async(self, data: dict, token: str):
        """Execute one-click payment

        https://docs.maibmerchants.md/en/one-click-payments/execute-one-click-payment"""

        return await self._execute_pay_operation_async(endpoint=MaibSdk.EXE_ONECLICK, data=data, token=token, required_params=MaibApi.REQUIRED_EXECUTE_ONECLICK_PARAMS)
    #endregion

    #region Deleting the card from maib ecomm
    def delete_card(self, entity_id: str, token: str):
        """Deleting the card from maib ecomm

        https://docs.maibmerchants.md/en/deleting-the-card-from-maib-ecomm"""

        return self._execute_entity_id_operation(method='DELETE', endpoint=MaibSdk.DELETE_CARD, entity_id=entity_id, token=token)

    async def delete_card_async(self, entity_id: str, token: str):
        """Deleting the card from maib ecomm

        https://docs.maibmerchants.md/en/deleting-the-card-from-maib-ecomm"""

        return await self._execute_entity_id_operation_async(method='DELETE', endpoint=MaibSdk.DELETE_CARD, entity_id=entity_id, token=token)
    #endregion

    #region Sync operation
    def _execute_pay_operation(self, endpoint: str, data: dict, token: str, required_params: list[str], method: str = 'POST'):
        self._validate_pay_params(data=data, required_params=required_params)
        self._validate_access_token(token=token)
        return self._send_request(method=method, endpoint=endpoint, data=data, token=token)

    def _execute_entity_id_operation(self, endpoint: str, entity_id: str, token: str, method: str = 'GET'):
        self._validate_id_param(entity_id=entity_id)
        self._validate_access_token(token=token)
        return self._send_request(method=method, endpoint=endpoint, token=token, entity_id=entity_id)

    def _send_request(self, method: str, endpoint: str, token: str, data: dict = None, entity_id: str = None):
        """Sends a request to the specified endpoint."""

        try:
            response = self._client.send_request(method=method, url=endpoint, data=data, token=token, entity_id=entity_id)
        except Exception as ex:
            raise MaibPaymentException(f'HTTP error while sending {method} request to endpoint {endpoint}: {ex}') from ex

        return self._client.handle_response(response, endpoint)
    #endregion

    #region Async operation
    async def _execute_pay_operation_async(self, endpoint: str, data: dict, token: str, required_params: list[str], method: str = 'POST'):
        self._validate_pay_params(data=data, required_params=required_params)
        self._validate_access_token(token=token)
        return await self._send_request_async(method=method, endpoint=endpoint, data=data, token=token)

    async def _execute_entity_id_operation_async(self, endpoint: str, entity_id: str, token: str, method: str = 'GET'):
        self._validate_id_param(entity_id=entity_id)
        self._validate_access_token(token=token)
        return await self._send_request_async(method=method, endpoint=endpoint, token=token, entity_id=entity_id)

    async def _send_request_async(self, method: str, endpoint: str, token: str, data: dict = None, entity_id: str = None):
        """Sends async request to the specified endpoint."""

        try:
            response = await self._client.send_request_async(method=method, url=endpoint, data=data, token=token, entity_id=entity_id)
        except Exception as ex:
            raise MaibPaymentException(f'HTTP error while sending {method} request to endpoint {endpoint}: {ex}') from ex

        return self._client.handle_response(response, endpoint)
    #endregion

    #region Validation
    @staticmethod
    def _validate_access_token(token: str):
        """Validates the access token."""

        if not token or len(token) == 0:
            raise MaibPaymentException('Access token is not valid. It should be a non-empty string.')

    @staticmethod
    def _validate_id_param(entity_id: str):
        """Validates the ID parameter."""

        if not entity_id:
            raise MaibPaymentException('Missing ID.')

        if len(entity_id) == 0:
            raise MaibPaymentException('Invalid ID parameter. Should be string of 36 characters.')

    @staticmethod
    def _validate_pay_params(data: dict, required_params: list[str]):
        """Validates the parameters."""

        # Check that all required parameters are present
        for param in required_params:
            if data.get(param) is None:
                raise MaibPaymentException(f'Missing required parameter: {param}')

        # Check that parameters have the expected types and formats
        biller_id = data.get('billerId')
        if biller_id is not None:
            if not isinstance(biller_id, str) or len(biller_id) != 36:
                raise MaibPaymentException('Invalid \'billerId\' parameter. Should be a string of 36 characters.')

        biller_expiry = data.get('billerExpiry')
        if biller_expiry is not None:
            if not isinstance(biller_expiry, str) or len(biller_expiry) != 4:
                raise MaibPaymentException('Invalid \'billerExpiry\' parameter. Should be a string of 4 characters.')

        pay_id = data.get('payId')
        if pay_id is not None:
            if not isinstance(pay_id, str) or len(pay_id) > 36:
                raise MaibPaymentException('Invalid \'payId\' parameter. Should be a string of 36 characters.')

        confirm_amount = data.get('confirmAmount')
        if confirm_amount is not None:
            if not isinstance(confirm_amount, (float, int)) or confirm_amount < 0.01:
                raise MaibPaymentException('Invalid \'confirmAmount\' parameter. Should be a numeric value > 0.')

        amount = data.get('amount')
        if amount is not None:
            if not isinstance(amount, (float, int)) or amount < 1:
                raise MaibPaymentException('Invalid \'amount\' parameter. Should be a numeric value >= 1.')

        refund_amount = data.get('refundAmount')
        if refund_amount is not None:
            if not isinstance(refund_amount, (float, int)) or refund_amount < 0.01:
                raise MaibPaymentException('Invalid \'refundAmount\' parameter. Should be a numeric value > 0.')

        currency = data.get('currency')
        if currency is not None:
            if not isinstance(currency, str) or currency not in ['MDL', 'EUR', 'USD']:
                raise MaibPaymentException('Invalid \'currency\' parameter. Currency should be one of \'MDL\', \'EUR\', or \'USD\'.')

        client_ip = data.get('clientIp')
        if client_ip is not None:
            if not isinstance(client_ip, str):
                raise MaibPaymentException('Invalid \'clientIp\' parameter. Please provide a valid IP address.')

        language = data.get('language')
        if language is not None:
            if not isinstance(language, str) or len(language) != 2:
                raise MaibPaymentException('Invalid \'language\' parameter. Should be a string of 2 characters.')

        description = data.get('description')
        if description is not None:
            if not isinstance(description, str) or len(description) > 124:
                raise MaibPaymentException('Invalid \'description\' parameter. Should be a string and not exceed 124 characters.')

        client_name = data.get('clientName')
        if client_name is not None:
            if not isinstance(client_name, str) or len(client_name) > 128:
                raise MaibPaymentException('Invalid \'clientName\' parameter. Should be a string and not exceed 128 characters.')

        email = data.get('email')
        if email is not None:
            if not isinstance(email, str):
                raise MaibPaymentException('Invalid \'email\' parameter. Please provide a valid email address.')

        phone = data.get('phone')
        if phone is not None:
            if not isinstance(phone, str) or len(phone) > 40:
                raise MaibPaymentException('Invalid \'phone\' parameter. Phone number should not exceed 40 characters.')

        order_id = data.get('orderId')
        if order_id is not None:
            if not isinstance(order_id, str) or len(order_id) > 36:
                raise MaibPaymentException('Invalid \'orderId\' parameter. Should be a string and not exceed 36 characters.')

        delivery = data.get('delivery')
        if delivery is not None:
            if not isinstance(delivery, (float, int)) or delivery < 0:
                raise MaibPaymentException('Invalid \'delivery\' parameter. Delivery fee should be a numeric value >= 0.')

        items = data.get('items')
        if items is not None:
            if not isinstance(items, list) or len(items) == 0:
                raise MaibPaymentException('Invalid \'items\' parameter. Items should be a non-empty list.')

            for item in items:
                item_id = item.get('id')
                if item_id is not None:
                    if not isinstance(item_id, str) or len(item_id) > 36:
                        raise MaibPaymentException('Invalid \'id\' parameter in the \'items\' list. Should be a string and not exceed 36 characters.')

                item_name = item.get('name')
                if item_name is not None:
                    if not isinstance(item_name, str) or len(item_name) > 128:
                        raise MaibPaymentException('Invalid \'name\' parameter in the \'items\' list. Should be a string and not exceed 128 characters.')

                item_price = item.get('price')
                if item_price is not None:
                    if not isinstance(item_price, (float, int)) or item_price < 0:
                        raise MaibPaymentException('Invalid \'price\' parameter in the \'items\' list. Item price should be a numeric value >= 0.')

                quantity = item.get('quantity')
                if quantity is not None:
                    if not isinstance(quantity, int) or quantity < 0:
                        raise MaibPaymentException('Invalid \'quantity\' parameter in the \'items\' array. Item quantity should be a numeric value >= 0.')

        callback_url = data.get('callbackUrl')
        if callback_url is not None:
            if not isinstance(callback_url, str):
                raise MaibPaymentException('Invalid \'callbackUrl\' parameter. Should be a string url.')

        ok_url = data.get('okUrl')
        if ok_url is not None:
            if not isinstance(ok_url, str):
                raise MaibPaymentException('Invalid \'ok_url\' parameter. Should be a string url.')

        fail_url = data.get('failUrl')
        if fail_url is not None:
            if not isinstance(fail_url, str):
                raise MaibPaymentException('Invalid \'fail_url\' parameter. Should be a string url.')

        return True
    #endregion
