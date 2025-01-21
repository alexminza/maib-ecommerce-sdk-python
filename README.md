# Python SDK for maib ecommerce API
maib e-commerce API docs: [https://docs.maibmerchants.md](https://docs.maibmerchants.md)

## Installation
To easily install or upgrade to the latest release, use `pip`.
```shell
pip install --upgrade maib-ecommerce-sdk
```

## Getting started
Import SDK:

```python
from maib_ecommerce_sdk import MaibAuthRequest, MaibApiRequest
```

Add project configuration:

```python
import os

MAIB_PROJECT_ID = os.getenv('MAIB_PROJECT_ID')
MAIB_PROJECT_SECRET = os.getenv('MAIB_PROJECT_SECRET')
MAIB_SIGNATURE_KEY = os.getenv('MAIB_SIGNATURE_KEY')
```

## SDK usage examples
### Get Access Token with Project ID and Project Secret

```python
maib_auth = MaibAuthRequest.create().generate_token(MAIB_PROJECT_ID, MAIB_PROJECT_SECRET)

maib_token = maib_auth['accessToken']
maib_refresh_token = maib_auth['refreshToken']
```

### Get Access Token with Refresh Token

```python
maib_auth = MaibAuthRequest.create().generate_token(maib_refresh_token)

maib_token = maib_auth['accessToken']
maib_refresh_token = maib_auth['refreshToken']
```

### Direct Payment

```python
# Set up required payment parameters
maib_pay_data = {
    'amount': 10.25,
    'currency': 'EUR',
    'clientIp': '127.0.0.1'
}

# Initiate Direct Payment
maib_pay = MaibApiRequest.create().pay(maib_pay_data, maib_token)

maib_pay_url = maib_pay['payUrl']
maib_pay_id = maib_pay['payId']
```

For more examples see [PHP SDK for maib ecommerce API](https://github.com/maib-ecomm/maib-sdk-php)
