import common

import api
import parser
import server

def run():
	common.config.init()
	common.models.init()
	
	#parser.init()
	server.run()