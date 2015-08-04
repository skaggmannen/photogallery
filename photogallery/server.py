import logging
import os
import signal

import tornado.httpserver
import tornado.ioloop
import tornado.web

from photogallery.common import config, models
from photogallery.api import photo

log = logging.getLogger(__name__)

handlers = [
	photo.PhotoListHandler,
	photo.PhotoDetailsHandler,
]

routes = [
	(r"/thumbs/(.*)", tornado.web.StaticFileHandler, {"path": config.THUMBS_DIR})
]
routes.extend([
	(config.API_URL_BASE + h.url, h) for h in handlers
])

settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static") # Serve static files from "./static" in module dir
}

def add_dynamic_handlers(app):
	session = models.Session()
	folders = session.query(models.Folder).all()

	handlers = []
	for folder in folders:
		log.info("Serving from folder: %s", folder.path)
		handlers.append(
			("/dynamic/{}/(.*)".format(folder.hash), tornado.web.StaticFileHandler, {"path": folder.path})
		)
	if len(handlers) > 0:
		app.add_handlers(".*$", handlers)

def sigint_handler():
	log.info("Closing down...")
	tornado.ioloop.IOLoop.instance().stop()

def run():
	app = tornado.web.Application(routes, **settings)

	add_dynamic_handlers(app)

	ioloop = tornado.ioloop.IOLoop.instance()

	signal.signal(signal.SIGINT, lambda sig, frame: ioloop.add_callback_from_signal(sigint_handler))

	server = tornado.httpserver.HTTPServer(app)
	server.listen(5000)
	
	ioloop.start()

if __name__ == "__main__":
	import sys

	if "debug" in sys.argv:
		settings["debug"] = True


	config.init()
	models.init()

	run()