import logging
from os.path import abspath, dirname, join

file_name = "cppg.log"
logger_path = join(dirname(abspath(__file__)), file_name)

def setup_logger():
    file_format = logging.Formatter("%(filename)s :: %(levelname)s\n%(message)s\n")

    file_handler = logging.FileHandler(logger_path, mode="a")
    file_handler.setFormatter(file_format)  
    file_handler.setLevel(logging.INFO)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    return logger

def clear_log():
    with open(logger_path, 'w'):
        pass

if __name__ == "__main__":
    logger = setup_logger()
    logger.info("fsdjlkfd")
