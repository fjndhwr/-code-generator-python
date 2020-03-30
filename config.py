# coding=utf-8
class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:XMlianluoyimysql!!!@192.168.8.90:32098/new_skin_wechat_service_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopConfig(Config):
    DEBUG = True


class ProductConfig(Config):
    pass
