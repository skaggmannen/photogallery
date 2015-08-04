import common
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)8s] - %(filename)12s: %(message)s')

import api
import parser
import server

def run():
	common.config.init()
	common.models.init()
	
	parser.run()
	server.run()