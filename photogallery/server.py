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

def create_links():
	session = models.Session()
	folders = session.query(models.Folder).all()

	for folder in folders:
		log.info("Checking symlink for folder: %s", folder.path)
		link_path = os.path.join(config.STATIC_DIR, folder.hash)
		if not os.path.exists(link_path):
			common.symlink(folder.path, link_path)
			log.info("Symlink created: %s", link_path)

def run(debug=False):
	#create_links()

	server = tornado.httpserver.HTTPServer(web_app)
	server.listen(5000)
	tornado.ioloop.IOLoop.current().start()