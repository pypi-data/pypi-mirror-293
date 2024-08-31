import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from .configuration import cfg

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def create_folder(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


class Logger:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, script_name):
        self.__path = cfg.parameters['log']['folder']['path']
        self.__name = cfg.parameters['log']['folder']['name']
        self.__filename = self.__path + os.sep + self.__name
        self.__formatter = cfg.parameters['log']['formatter']
        self.__log_size = cfg.parameters['log']['RotatingFileHandler']['file_size']
        self.__backup_count = cfg.parameters['log']['RotatingFileHandler']['backup_count']

        # Create folder is not exist
        create_folder(self.__path)

        # Create a _logger
        self.__logger = logging.getLogger(script_name)

        # Load Configuration
        self.__configure()

    def __configure(self):
        # set Level
        self.__logger.setLevel(logging.INFO)

        # Create a file handler
        file_handler = RotatingFileHandler(self.__filename,
                                           maxBytes=self.__log_size,
                                           backupCount=self.__backup_count)
        file_handler.setLevel(logging.INFO)

        # Create a stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)

        # Create a formatter
        formatter = logging.Formatter(self.__formatter)

        # Add the formatter to the handlers
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        # Add the handlers to the _logger
        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(stream_handler)

    def get_logger(self) -> object:
        return self.__logger
