import logging
from constant import logger as con_logger
from util.design_pattern import Singleton
import os

@Singleton
class Logger:
	def __init__(self, path):
		out_location = os.path.join(path, con_logger.LOG_FILE_NAME)
		self.logging = logging.basicConfig(filename=out_location, level=logging.DEBUG)

	def error(self, message):
		self.logging.error(message)

	def warning(self, message):
		self.logging.warning(message)

	def info(self, message):
		self.logging.info(message)