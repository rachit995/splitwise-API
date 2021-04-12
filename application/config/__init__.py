import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    MONGO_URI = "mongodb+srv://" + os.environ.get("MONGO_USER") + \
        ":" + os.environ.get("MONGO_PASSWORD") + \
        "@" + os.environ.get("MONGO_HOST") + "/" + \
        os.environ.get("MONGO_DB") + "?retryWrites=true&w=majority"


class ProductionConfig(Config):
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", False)


class DevelopmentConfig(Config):
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
