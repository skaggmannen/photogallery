import logging
import os

import tornado.httpserver
import tornado.ioloop
import tornado.web

from photogallery import api, common, config, models

log = logging.getLogger(__name__)

handlers = [
	api.photo.PhotoListHandler,
	api.photo.PhotoDetailsHandler,
]

routes = [
	(r"/dynamic/(.*)", tornado.web.StaticFileHandler, {"path": config.STATIC_DIR})
]
routes.extend([
	#(config.API_URL_BASE + h.url, h) for h in handlers
])

settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static") # Serve static files from "./static" in module dir
}

web_app = tornado.web.Application(routes, **settings)

def add_dynamic_handlers():
	session = models.Session()
	folders = session.query(models.Folder).all()

	handlers = []
	for folder in folders:
		log.info("Serving from folder: %s", folder.path)
		handlers.append(
			("/dynamic/{}/(.*)".format(folder.hash), tornado.web.StaticFileHandler, {"path": folder.path})
		)
	if len(handlers) > 0:
		web_app.add_handlers(".*$", handlers)

def run(debug=False):
	add_dynamic_handlers()

	server = tornado.httpserver.HTTPServer(web_app)
	server.listen(5000)
	tornado.ioloop.IOLoop.current().start()