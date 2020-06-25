# config.y
class Config(object):
    """
    TBD
    """
class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config ={
    'development': DevelopmentConfig,
    'production': ProductionConfig
}