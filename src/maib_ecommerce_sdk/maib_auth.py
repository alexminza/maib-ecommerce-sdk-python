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
    _client: MaibSdk = None

    def __init__(self, client: MaibSdk):
        self._client = client

    def generate_token(self, project_id: str = None, project_secret: str = None):
        """Generates a new access token using the given project ID and secret or refresh token."""

        if project_id is None and project_secret is None:
            raise MaibTokenException('Project ID and Project Secret or Refresh Token are required.')

        post_data = {}
        if project_id is not None and project_secret is not None:
            post_data['projectId'] = project_id
            post_data['projectSecret'] = project_secret
        elif project_id is not None and project_secret is None:
            post_data['refreshToken'] = project_id

        try:
            method = 'POST'
            endpoint = MaibSdk.GET_TOKEN
            response = self._client.send_request(method=method, url=endpoint, data=post_data)
        except Exception as ex:
            logger.exception(self.generate_token.__qualname__)
            raise MaibTokenException(f'HTTP error while sending {method} request to endpoint {endpoint}: {ex}') from ex

        result = self._client.handle_response(response, MaibSdk.GET_TOKEN)
        return result
