import logging
import os
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)8s] - %(filename)12s: %(message)s')

log = logging.getLogger(__name__)

DEBUG = False

CONFIG_DIR = os.path.expanduser("~/.photogallery/")
STATIC_DIR = os.path.join(CONFIG_DIR, "static")

THUMBS_DIR = os.path.join(CONFIG_DIR, "thumbs")
THUMBS_SIZE = (400, 400)

API_URL_BASE = "/api/v1"

DB_STRING = "sqlite:///{}/test.db".format(CONFIG_DIR)

def init():
	if "debug" in sys.argv:
		logging.getLogger().setLevel(logging.DEBUG)
		DEBUG = True

	if not os.path.exists(CONFIG_DIR):
		log.info("Creating config directory: %s", CONFIG_DIR)
		os.makedirs(CONFIG_DIR)
	if not os.path.exists(STATIC_DIR):
		log.info("Creating static directory: %s", STATIC_DIR)
		os.makedirs(STATIC_DIR)
	if not os.path.exists(THUMBS_DIR):
		log.info("Creating thumb directory: %s", THUMBS_DIR)
		os.makedirs(THUMBS_DIR)

