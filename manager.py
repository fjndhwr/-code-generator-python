from flask import Flask
from werkzeug.routing import BaseConverter
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class HTMLConverter(BaseConverter):
    regex = '.*'


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.url_map.converters['html'] = HTMLConverter

    # # 日志处理
    # import logging
    # from logging.handlers import RotatingFileHandler
    # logging.basicConfig(level=logging.DEBUG)
    # file_log_handler = RotatingFileHandler(os.path.join(BASE_DIR, "logs/ihome.log"), maxBytes=1024 * 1024 * 100,
    #                                        backupCount=10)
    # formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # file_log_handler.setFormatter(formatter)
    # logging.getLogger().addHandler(file_log_handler)

    return app

