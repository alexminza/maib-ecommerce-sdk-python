"""Python SDK for maib ecommerce API"""

import logging

from .maib_sdk import MaibSdk, MaibTokenException

logger = logging.getLogger(__name__)


class MaibAuthRequest:
    """Factory class responsible for creating new instances of the MaibAuth class."""

    @staticmethod
    def create():
        """Creates an instance of the MaibAuth class."""

        client = MaibSdk()
        return MaibAuth(client)

class MaibAuth:
    """https://docs.maibmerchants.md/e-commerce/access-token-generation"""

    _client: MaibSdk = None

    def __init__(self, client: MaibSdk):
        self._client = client

    #region Generate token API
    def generate_token(self, project_id: str, project_secret: str):
        """Token generation using Project ID and Project Secret

        https://docs.maibmerchants.md/e-commerce/access-token-generation#token-generation-using-project-id-and-project-secret"""

        token_data = self._build_generate_token_data(
            project_id=project_id,
            project_secret=project_secret)

        return self._generate_token(data=token_data)

    async def generate_token_async(self, project_id: str, project_secret: str):
        """Token generation using Project ID and Project Secret

        https://docs.maibmerchants.md/e-commerce/access-token-generation#token-generation-using-project-id-and-project-secret"""

        token_data = self._build_generate_token_data(
            project_id=project_id,
            project_secret=project_secret)

        return await self._generate_token_async(data=token_data)

    @classmethod
    def _build_generate_token_data(cls, project_id: str, project_secret: str):
        if not project_id or not project_secret:
            raise MaibTokenException('Project ID and Project Secret are required.')

        token_data = {
            'projectId': project_id,
            'projectSecret': project_secret
        }

        return token_data
    #endregion

    #region Refresh token API
    def refresh_token(self, refresh_token: str):
        """Token generation using Refresh Token

        https://docs.maibmerchants.md/e-commerce/access-token-generation#token-generation-using-refresh-token"""

        token_data = self._build_refresh_token_data(refresh_token=refresh_token)
        return self._generate_token(data=token_data)

    async def refresh_token_async(self, refresh_token: str):
        """Token generation using Refresh Token

        https://docs.maibmerchants.md/e-commerce/access-token-generation#token-generation-using-refresh-token"""

        token_data = self._build_refresh_token_data(refresh_token=refresh_token)
        return await self._generate_token_async(data=token_data)

    @classmethod
    def _build_refresh_token_data(cls, refresh_token: str):
        if not refresh_token:
            raise MaibTokenException('Refresh token is required.')

        token_data = {
            'refreshToken': refresh_token
        }

        return token_data
    #endregion

    #region Generate token
    def _generate_token(self, data: dict):
        try:
            method = 'POST'
            endpoint = MaibSdk.GENERATE_TOKEN
            response = self._client.send_request(method=method, url=endpoint, data=data)
        except Exception as ex:
            logger.exception(self.__class__.__qualname__)
            raise MaibTokenException(f'HTTP error while sending {method} request to endpoint {endpoint}: {ex}') from ex

        result = self._client.handle_response(response, MaibSdk.GENERATE_TOKEN)
        return result

    async def _generate_token_async(self, data: dict):
        try:
            method = 'POST'
            endpoint = MaibSdk.GENERATE_TOKEN
            response = await self._client.send_request_async(method=method, url=endpoint, data=data)
        except Exception as ex:
            logger.exception(self.__class__.__qualname__)
            raise MaibTokenException(f'HTTP error while sending {method} request to endpoint {endpoint}: {ex}') from ex

        result = self._client.handle_response(response, MaibSdk.GENERATE_TOKEN)
        return result
    #endregion
