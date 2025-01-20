import logging
from .maibsdk import MAIBSDK, MAIBTokenException

class MAIBAuthRequest:
    @staticmethod
    def create():
        client = MAIBSDK()
        return MAIBAuth(client)

class MAIBAuth:
    client: MAIBSDK = None

    def __init__(self, client: MAIBSDK):
        self.client = client

    def generate_token(self, project_id: str = None, project_secret: str = None):
        if project_id is None and project_secret is None:
            raise MAIBTokenException('Project ID and Project Secret or Refresh Token are required.')

        post_data = {}
        if project_id is not None and project_secret is not None:
            post_data['projectId'] = project_id
            post_data['projectSecret'] = project_secret
        elif project_id is not None and project_secret is None:
            post_data['refreshToken'] = project_id

        try:
            response = self.client.send_request('POST', MAIBSDK.GET_TOKEN, post_data)
        except Exception as ex:
            logging.exception('MAIBAuth.generate_token')
            raise MAIBTokenException(f'HTTP error while sending POST request to endpoint {MAIBSDK.GET_TOKEN}') from ex

        result = self.client.handle_response(response, MAIBSDK.GET_TOKEN)
        return result
