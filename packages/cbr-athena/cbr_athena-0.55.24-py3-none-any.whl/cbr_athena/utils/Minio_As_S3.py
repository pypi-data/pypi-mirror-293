import requests

from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Status import status_ok, status_error


class Minio_As_S3(Type_Safe):

    @cache_on_self
    def server_online(self):
        return self.connect_to_server().get('status') == 'ok'

    def connect_to_server(self):
        try:
            response = requests.get(self.url_server())
            # Check if the status code is 200, indicating MinIO is up and running
            if response.status_code == 200:
                return status_ok(message="MinIO console is accessible on port 9001")
            return status_error(message="Server returned status code {response.status_code}")
        except requests.exceptions.ConnectionError as e:
            return status_error(message=f"Could not connect to MinIO console on port 9001: {e}")


    def url_server(self):
        return 'http://localhost:9001'
