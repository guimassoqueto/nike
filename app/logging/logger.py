from sys import stdout
import logging


def getLogger(name: str):
  formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s - %(message)s')
  logger_handler = logging.StreamHandler(stdout)
  logger_handler.setFormatter(formatter)
     
  logger = logging.getLogger(name)
  logger.setLevel(logging.DEBUG)
  logger.addHandler(logger_handler)
  
  return logger