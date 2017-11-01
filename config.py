import os


def is_development():
    mode = os.getenv("MODE", "prod")
    return mode == "dev"


def get_mandatory_env(key):
    value = os.getenv(key)
    if value is None:
        raise ValueError("Environment variable " + key + " is missing")
    return value


class ApplicationConfig(object):
    __instance = None

    def __init__(self):
        self._log_connection_string = None
        self._log_database = None
        self._temp_folder = None

    @staticmethod
    def get_config():
        if ApplicationConfig.__instance is None:
            ApplicationConfig.__instance = ApplicationConfig()
        return ApplicationConfig.__instance

    def log_connection_string(self):
        if self._log_connection_string is None:
            self._log_connection_string = os.getenv("LOG_CONNECTION_STRING", "")
        return self._log_connection_string

    def log_database(self):
        if self._log_database is None:
            self._log_database = os.getenv("LOG_DATABASE", "log")
        return self._log_database

    def temp_folder(self):
        if self._temp_folder is None:
            self._temp_folder = get_mandatory_env("TEMP_FOLDER")
        return self._temp_folder


DEBUG = is_development()
