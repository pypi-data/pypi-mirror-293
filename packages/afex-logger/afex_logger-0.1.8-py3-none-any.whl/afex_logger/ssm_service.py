import json

import boto3


class SsmService:

    def __init__(self, region_name, access_key, secret_key, session_token):
        session = boto3.session.Session()
        self.client = session.client(
            service_name='secretsmanager',
            region_name=region_name,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token,
        )

    buckets = {}

    def retrieve_ssm_secrets(self, secret_name, uses_cache=True):
        if uses_cache and secret_name in self.buckets and self.buckets[secret_name]:
            return None

        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
        except Exception as e:
            return str(e)

        secret = get_secret_value_response.get('SecretString')
        self.buckets[secret_name] = json.loads(secret)

        return None

    def get_secret_value(self, secret_name, key_name, uses_cache=True):
        error = self.retrieve_ssm_secrets(secret_name, uses_cache=uses_cache)
        if error:
            return None, error

        return self.buckets[secret_name].get(key_name), None
