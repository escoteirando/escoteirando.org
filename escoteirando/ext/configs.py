"""
Configurations read by environment variables
"""

import os

import dotenv

from escoteirando.cross_cutting.tools import Singleton


@Singleton
class Configs:

    def __init__(self):
        self.MAIL_SERVER: str = None
        self.MAIL_PORT: int = 0
        self.MAIL_USE_TLS: bool = False
        self.MAIL_USE_SSL: bool = False
        self.MAIL_USERNAME: str = None
        self.MAIL_PASSWORD: str = None
        self.MAIL_USER_FROM: str = None

        self.CACHE_STRING_CONNECTION: str = None

        self.load()

    def load(self):
        dotenv.load_dotenv()
        self.MAIL_SERVER = self.getenv('MAIL_SERVER', None)
        self.MAIL_PORT = self.getenv('MAIL_PORT', '0', int)
        self.MAIL_USE_TLS = self.getenv('MAIL_USE_TLS', '0', bool)
        self.MAIL_USE_SSL = self.getenv('MAIL_USE_SSL', '0', bool)
        self.MAIL_USERNAME = self.getenv('MAIL_USERNAME', None)
        self.MAIL_PASSWORD = self.getenv('MAIL_PASSWORD', None)
        self.MAIL_USER_FROM = self.getenv('MAIL_USER_FROM', None)

        self.CACHE_STRING_CONNECTION = self.getenv(
            'CACHE_STRING_CONNECTION', 'path://.cache')

    def getenv(self, key: str, default, data_type=str):
        value = os.getenv(key, default)
        if data_type == bool:
            return (value.upper()+'0')[0] in ['1', 'T', 'Y', 'S']
        elif data_type == int:
            return int(value)

        return value

    def get_configs(self, *key_names) -> list:
        """Get a list of values from keys informed"""
        return [getattr(self, key_name) if hasattr(self, key_name)
                else None
                for key_name in key_names]


def init_app(app):
    app.configs = Configs.Instance()
