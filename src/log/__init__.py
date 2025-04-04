import logging
from os.path import abspath, dirname, join

file_name = "logs.log"
logger_path = join(dirname(abspath(__file__)), file_name)

def setup_logger():
    file_format = logging.Formatter(fmt="%(filename)s :: %(levelname)s\n%(message)s\n",
                                    datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = logging.FileHandler(logger_path, mode="a")
    file_handler.setFormatter(file_format)  
    file_handler.setLevel(logging.INFO)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        logger.addHandler(file_handler)
    return logger

def clear_log():
    with open(logger_path, 'w'):
        pass