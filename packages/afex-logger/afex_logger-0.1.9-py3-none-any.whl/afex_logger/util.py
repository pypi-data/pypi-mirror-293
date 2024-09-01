import decimal
import json
from abc import abstractmethod
from datetime import datetime, date
from pydoc import locate
from typing import List
from uuid import UUID

from django.conf import settings
from django.db.models import TextChoices
from django.utils import timezone

from afex_logger.log_service import AppLogService
from afex_logger.tasks import submit_log_data


class LogTypes(TextChoices):
    requests = "requests"
    process = "process"
    errors = "errors"
    activities = "activities"


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, UUID):
            return str(o)
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, date):
            return o.isoformat()
        elif hasattr(o, '__dict__'):
            return o.__dict__.get('name', '')
        return super(DecimalEncoder, self).default(o)


class ConfigProvider:
    """
    Configuration Provider for logger
    """

    @abstractmethod
    def get_api_key(self):
        raise NotImplementedError("Please implement this method")

    @abstractmethod
    def get_base_url(self):
        raise NotImplementedError("Please implement this method")

    @classmethod
    def is_debug_mode(cls) -> bool:
        return False

    @classmethod
    def get_excluded_path_patterns(cls):
        return ["/logs/", 'media/', "static/"]

    @classmethod
    def get_excluded_request_method(cls) -> List[str]:
        return ['HEAD', 'OPTIONS', 'TRACE']

    @classmethod
    def get_rest_content_types(cls) -> List[str]:
        return []

    @classmethod
    def get_excluded_data_fields(cls):
        return ['password', 'csrfmiddlewaretoken']

    @classmethod
    def get_api_path_prefix(cls):
        return "/api/"


class LogUtil:

    @classmethod
    def submit_error_log(cls, data):
        submit_log_data.delay(LogTypes.errors, json.dumps(data, cls=DecimalEncoder))

    @classmethod
    def submit_activity_log(cls, data):
        submit_log_data.delay(LogTypes.activities, json.dumps(data, cls=DecimalEncoder))

    @classmethod
    def submit_process_log(cls, data):
        submit_log_data.delay(LogTypes.process, json.dumps(data, cls=DecimalEncoder))

    @classmethod
    def submit_requests_log(cls, data):
        task_id = submit_log_data.delay(LogTypes.requests, json.dumps(data, cls=DecimalEncoder))
        config_util = cls.get_config_provider()
        if config_util.is_debug_mode():
            cls.debug_print(task_id)

    @classmethod
    def fetch_error_logs(cls, params):
        return AppLogService().fetch_logs(LogTypes.errors, params)

    @classmethod
    def fetch_activity_logs(cls, params):
        return AppLogService().fetch_logs(LogTypes.activities, params)

    @classmethod
    def fetch_process_logs(cls, params):
        return AppLogService().fetch_logs(LogTypes.process, params)

    @classmethod
    def fetch_request_logs(cls, params):
        return AppLogService().fetch_logs(LogTypes.requests, params)

    @classmethod
    def debug_print(cls, *args):
        print("Log Service::[{}]".format(timezone.now()), *args)

    @staticmethod
    def get_config_provider() -> ConfigProvider:
        try:
            app_config_provider_loc = getattr(settings, "LOG_CONFIG_PROVIDER")
            if isinstance(app_config_provider_loc, str):
                app_config_provider = locate(app_config_provider_loc)
            else:
                app_config_provider = app_config_provider_loc

            return app_config_provider()
        except Exception as _:
            raise NotImplementedError(
                "Ensure you add 'LOG_CONFIG_PROVIDER' to your django settings. "
                "This class must  extend ConfigProvider"
            )
