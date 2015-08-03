import logging
import os

log = logging.getLogger(__name__)

DEBUG = True

CONFIG_DIR = os.path.expanduser("~/.photogallery/")
STATIC_DIR = "{}/static/".format(CONFIG_DIR)

API_URL_BASE = "/api/v1"

DB_STRING = "sqlite:///{}/test.db".format(CONFIG_DIR)

def init():
	if not os.path.exists(CONFIG_DIR):
		log.info("Creating config directory: %s", CONFIG_DIR)
		os.makedirs(CONFIG_DIR)
	if not os.path.exists(STATIC_DIR):
		log.info("Creating static directory: %s", STATIC_DIR)
		os.makedirs(STATIC_DIR)
