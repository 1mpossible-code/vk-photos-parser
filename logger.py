import logging
import os

from services.PathService import get_app_path

os.chdir(get_app_path())


def create_logger(name):
    # Create a custom logger
    local_logger = logging.getLogger(name)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('logs.log')

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    local_logger.addHandler(c_handler)
    local_logger.addHandler(f_handler)

    local_logger.setLevel(logging.INFO)

    return local_logger
