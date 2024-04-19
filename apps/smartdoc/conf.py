# !/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""
配置分类：
1. Django使用的配置文件，写到settings中
2. 程序需要, 用户不需要更改的写到settings中
3. 程序需要, 用户需要更改的写到本config中
"""
import errno
import logging
import os
import re
from importlib import import_module
from urllib.parse import urljoin, urlparse
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
logger = logging.getLogger('max_kb')


def import_string(dotted_path):
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError(
            'Module "%s" does not define a "%s" attribute/class' %
            (module_path, class_name)) from err


def is_absolute_uri(uri):
    """ 判断一个uri是否是绝对地址 """
    if not isinstance(uri, str):
        return False

    result = re.match(r'^http[s]?://.*', uri)
    if result is None:
        return False

    return True


def build_absolute_uri(base, uri):
    """ 构建绝对uri地址 """
    if uri is None:
        return base

    if isinstance(uri, int):
        uri = str(uri)

    if not isinstance(uri, str):
        return base

    if is_absolute_uri(uri):
        return uri

    parsed_base = urlparse(base)
    url = "{}://{}".format(parsed_base.scheme, parsed_base.netloc)
    path = '{}/{}/'.format(parsed_base.path.strip('/'), uri.strip('/'))
    return urljoin(url, path)


class DoesNotExist(Exception):
    pass


class Config(dict):
    defaults = {
        # 数据库相关配置
        "DB_HOST": "",
        "DB_PORT": "",
        "DB_USER": "",
        "DB_PASSWORD": "",
        "DB_ENGINE": "django.db.backends.postgresql_psycopg2",

        # 邮件相关配置
        "EMAIL_ADDRESS": "",
        "EMAIL_USE_TLS": False,
        "EMAIL_USE_SSL": True,
        "EMAIL_HOST": "",
        "EMAIL_PORT": 465,
        "EMAIL_HOST_USER": "",
        "EMAIL_HOST_PASSWORD": "",

        # 向量模型
        "EMBEDDING_MODEL_ONLINE": "false",
        "EMBEDDING_MODEL_NAME": "shibing624/text2vec-base-chinese",
        "EMBEDDING_DEVICE": "cpu",
        "EMBEDDING_MODEL_PATH": os.path.join(PROJECT_DIR, 'models'),

        # 项目配置
        "DEBUG": False,

        "TIME_ZONE": "Asia/Shanghai",

        # 向量库配置
        "VECTOR_STORE_NAME": 'pg_vector',

        # openai
        "OPENAI_BASE_URL": "",
        "OPENAI_API_KEY": "",
        "OPENAI_MAX_TOKEN": 4096,

        # rag
        "RAG_SIMILARITY": 0.7,
        "RAG_TOP_K": 10,
        "RAG_FUSION": True,

    }

    def get_debug(self) -> bool:
        return self.get('DEBUG') if 'DEBUG' in self else True

    def get_time_zone(self) -> str:
        return self.get('TIME_ZONE') if 'TIME_ZONE' in self else 'Asia/Shanghai'

    def get_db_setting(self) -> dict:
        return {
            "NAME": self.get('DB_NAME'),
            "HOST": self.get('DB_HOST'),
            "PORT": self.get('DB_PORT'),
            "USER": self.get('DB_USER'),
            "PASSWORD": self.get('DB_PASSWORD'),
            "ENGINE": self.get('DB_ENGINE')
        }

    def get_openai_setting(self) -> dict:
        return {
            "BASE_URL": self.get('OPENAI_BASE_URL'),
            "API_KEY": self.get('OPENAI_API_KEY'),
        }

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))

    def __getitem__(self, item):
        return self.get(item)

    def __getattr__(self, item):
        return self.get(item)


class ConfigManager:
    config_class = Config

    def __init__(self, root_path=None):
        self.root_path = root_path
        self.config = self.config_class()
        for key in self.config_class.defaults:
            self.config[key] = self.config_class.defaults[key]

    def from_mapping(self, *mapping, **kwargs):
        """Updates the config like :meth:`update` ignoring items with non-upper
        keys.

        .. versionadded:: 0.11
        """
        mappings = []
        if len(mapping) == 1:
            if hasattr(mapping[0], 'items'):
                mappings.append(mapping[0].items())
            else:
                mappings.append(mapping[0])
        elif len(mapping) > 1:
            raise TypeError(
                'expected at most 1 positional argument, got %d' % len(mapping)
            )
        mappings.append(kwargs.items())
        for mapping in mappings:
            for (key, value) in mapping:
                if key.isupper():
                    self.config[key] = value
        return True

    def load_from_yml(self):
        yaml_path = os.path.join(PROJECT_DIR, 'config.yaml')
        try:
            if not os.path.isfile(yaml_path):
                raise FileNotFoundError(f"No such file: '{yaml_path}'")
            with open(yaml_path, 'r') as file:
                obj = yaml.safe_load(file)
            if not isinstance(obj, dict):
                raise ValueError("YAML content is invalid or not a dictionary")
            return self.from_mapping(obj)
        except (FileNotFoundError, IOError, yaml.YAMLError, ValueError) as e:
            # Handle specific errors related to file I/O and YAML parsing
            raise RuntimeError(f"Configuration load failed: {e}") from e

    @classmethod
    def load_user_config(cls, root_path=None, config_class=None):
        config_class = config_class or Config
        cls.config_class = config_class
        if not root_path:
            root_path = PROJECT_DIR
        manager = cls(root_path=root_path)
        if manager.load_from_yml():
            config = manager.config
        else:
            msg = f"""

            Error: No config file found.

            You can run `cp config_example.yml {root_path}/config.yml`, and edit it.

            """
            raise ImportError(msg)
        print(f"load config from {root_path}/config.yml, config content:{config}")
        logger.info(f"load config from ${root_path}/config.yml, config content:${config}")
        return config
