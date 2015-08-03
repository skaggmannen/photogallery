import models
import parser
import server

def run():
	models.init()
	#parser.init()
	server.run()