import sqlalchemy

import tornado.httpserver
import tornado.ioloop
import tornado.web

import app.config
import app.api.photo

handlers = [
	api.photo.PhotoListHandler,
	api.photo.PhotoDetailsHandler,
]

routes = [
	(r"/static/(.*)", tornado.web.StaticFileHandler, {"path": app.config.STATIC_DIR})
]
routes.extend([
	(app.config.API_URL_BASE + h.url, h) for h in handlers
])

web_app = tornado.web.Application(routes)

engine = sqlalchemy.create_engine(app.config.DB_STRING)
models.Session.configure(bind=engine)

class App:
	def run(self, debug=False):
		models.Base.metadata.create_all()

		server = tornado.httpserver.HTTPServer(web_app)
		server.listen(5000)
		tornado.ioloop.IOLoop.current().start()

app = App()