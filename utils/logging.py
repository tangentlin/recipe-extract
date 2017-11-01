import logging
from log4mongo.handlers import MongoHandler
from config import ApplicationConfig


class Logger(object):
    def __init__(self):
        self.name = 'recipe-extract-api-service'

    def getLogger(self):
        return logging.getLogger(self.name)

    def setupLogger(self):
        logger = self.getLogger()
        logger.setLevel(logging.DEBUG)

        config = ApplicationConfig.get_config()

        log_connection_string = config.log_connection_string()
        if log_connection_string is not None and log_connection_string != "":
            mongo_handler = MongoHandler(host=log_connection_string, database_name=config.log_database())
            mongo_handler.setLevel(logging.DEBUG)
            logger.addHandler(mongo_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)

        return logger
