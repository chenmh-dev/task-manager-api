import os
class BaseConfig:
    ENV_NAME = "base"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    

class DevelopmentConfig(BaseConfig):
    ENV_NAME = "development"
    DEBUG = True

class ProductionConfig(BaseConfig):
    ENV_NAME = "production"
    DEBUG = False