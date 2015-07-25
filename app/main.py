import sqlalchemy

import tornado.httpserver
import tornado.ioloop
import tornado.web

from photogallery import settings
from photogallery.api import photo

handlers = [
	photo.PhotoListHandler,
	photo.PhotoDetailsHandler,
]

routes = [
	(r"/static/(.*)", tornado.web.StaticFileHandler, {"path": settings.STATIC_DIR})
]

app = tornado.web.Application(
	[(settings.API_URL_BASE + h.url, h) for h in handlers]
)

engine = sqlalchemy.create_engine(settings.DB_STRING)
models.Session.configure(bind=engine)

if __name__ == "__main__":
	models.Base.metadata.create_all()

	server = tornado.httpserver.HTTPServer(app)
	server.listen(5000)
	tornado.ioloop.IOLoop.current().start()
