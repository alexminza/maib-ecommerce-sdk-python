"""Python SDK for maib ecommerce API"""

from .maib_sdk import MaibSdk, MaibTokenException


class MaibAuthRequest:
    """Factory class responsible for creating new instances of the MaibAuth class."""

    @staticmethod
    def create():
        """Creates an instance of the MaibAuth class."""

        client = MaibSdk()
        return MaibAuth(client)

class MaibAuth:
    _client: MaibSdk = None

    def __init__(self, client: MaibSdk):
        self._client = client

    #region Generate token API
    def generate_token(self, project_id: str = None, project_secret: str = None):
        """Generates a new access token using the given project ID and secret or refresh token.

        https://docs.maibmerchants.md/en/access-token-generation"""

        generate_token_data = self._build_generate_token_data(
            project_id=project_id,
            project_secret=project_secret)

        try:
            method = 'POST'
            endpoint = MaibSdk.GET_TOKEN
            response = self._client.send_request(method=method, url=endpoint, data=generate_token_data)
        except Exception as ex:
            raise MaibTokenException(f'HTTP error while sending {method} request to endpoint {endpoint}: {ex}') from ex

        result = self._client.handle_response(response, MaibSdk.GET_TOKEN)
        return result

    async def generate_token_async(self, project_id: str = None, project_secret: str = None):
        """Generates a new access token using the given project ID and secret or refresh token.

        https://docs.maibmerchants.md/en/access-token-generation"""

        generate_token_data = self._build_generate_token_data(
            project_id=project_id,
            project_secret=project_secret)

        try:
            method = 'POST'
            endpoint = MaibSdk.GET_TOKEN
            response = await self._client.send_request_async(method=method, url=endpoint, data=generate_token_data)
        except Exception as ex:
            raise MaibTokenException(f'HTTP error while sending {method} request to endpoint {endpoint}: {ex}') from ex

        result = self._client.handle_response(response, MaibSdk.GET_TOKEN)
        return result

    @classmethod
    def _build_generate_token_data(cls, project_id: str, project_secret: str):
        if project_id is None and project_secret is None:
            raise MaibTokenException('Project ID and Project Secret or Refresh Token are required.')

        token_data = {}
        if project_id is not None and project_secret is not None:
            token_data['projectId'] = project_id
            token_data['projectSecret'] = project_secret
        elif project_id is not None and project_secret is None:
            token_data['refreshToken'] = project_id

        return token_data
    #endregion
