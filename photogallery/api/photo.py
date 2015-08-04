import hashlib
import logging
import os

log = logging.getLogger(__name__)

import sqlalchemy
import tornado.web

from photogallery.common import config, models
from photogallery.api import JsonRequestHandler

def photo_repr(p, f):
	if p.dir != "":
		rel_path = os.path.join(p.dir, p.name).encode("utf-8")
		print(rel_path)
	else:
		rel_path = p.name

	return {
		"url": config.API_URL_BASE + "/photo/{0}".format(p.id),
		"image": "/dynamic/{0}/{1}".format(f.hash, rel_path),
		"thumb": "/thumbs/{0}.jpg".format(p.md5),
		"path": os.path.join(f.path, p.dir, p.name).encode("utf-8"),
	}
	
class PhotoListHandler(JsonRequestHandler):
	url = r"/photo/"

	def get(self):
		session = models.Session()

		limit = self.get_query_argument("limit", default=100)
		offset = self.get_query_argument("offset", default=0)

		results = session.query(models.Photo, models.Folder).limit(limit).offset(offset).all()

		self.write({
			"photos": [photo_repr(p, f) for p, f in results]
		})
		self.finish()

	def post(self):
		session = models.Session()

		photos = []

		try:
			for data in self.json_args["photos"]:
				p = models.Photo()
				p.root_hash = hashlib.md5(data["root"]).hexdigest()
				p.root = data["root"]
				p.rel_path = data["rel_path"]

				photos.append(p)
		except KeyError as e:
			raise tornado.web.HTTPError(400)

		session.add_all(photos)
		session.commit()

		self.set_status(201)

		self.write({
			"photos": [API_URL_BASE + "/photo/{}".format(p.id) for p in photos]
		})
		self.finish()


class PhotoDetailsHandler(JsonRequestHandler):
	url = r"/photo/(?P<id>\d+)"

	def get(self, id=None):
		session = models.Session()

		try:
			p, f = session.query(models.Photo, models.Folder).filter_by(id=id).one()
		except sqlalchemy.orm.exc.MultipleResultsFound as e:
			raise tornado.web.HTTPError(500)
		except sqlalchemy.orm.exc.NoResultsFound as e:
			raise tornado.web.HTTPError(404)

		self.write(photo_repr(p, f))
		self.finish()

	def patch(self, id=None):
		session = models.Session()

		try:
			p, f = session.query(models.Photo, models.Folder).filter_by(id=id).one()
		except sqlalchemy.orm.exc.MultipleResultsFound as e:
			raise tornado.web.HTTPError(500)
		except sqlalchemy.orm.exc.NoResultsFound as e:
			raise tornado.web.HTTPError(404)

		if "date" in self.json_args:
			p.date = self.json_args["date"]
		if "orientation" in self.json_args:
			p.orientation = self.json_args["orientation"]

		session.commit()

		self.write(photo_repr(p, f))
		self.finish()
