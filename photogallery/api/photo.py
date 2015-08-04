import hashlib

import sqlalchemy
import tornado.web

from photogallery.common import config, models
from photogalleru.api import JsonRequestHandler

def photo_repr(p):
	return {
		"url": config.API_URL_BASE + "/photo/{}".format(p.id),
		"image": "/dynamic/{}/{}".format(p.root_hash, p.rel_path),
	}
	
class PhotoListHandler(JsonRequestHandler):
	url = r"/photo/"

	def get(self):
		session = models.Session()

		limit = self.get_query_argument("limit", default=100)
		offset = self.get_query_argument("offset", default=0)

		photos = session.query(models.Photo).limit(limit).offset(offset).all()

		return {
			"photos": [photo_repr(p) for p in photos]
		}

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

				session.add(p)

		except KeyError as e:
			raise tornado.web.HTTPError(400)

		session.commit()

		self.set_status(201)

		return {
			"photos": [API_URL_BASE + "/photo/{}".format(p.id) for p in photos]
		}


class PhotoDetailsHandler(JsonRequestHandler):
	url = r"/photo/(?P<id>\d+)"

	def get(self, id=None):
		session = models.Session()

		try:
			p = session.query(models.Photo).filter_by(id=id).one()
		except sqlalchemy.orm.exc.MultipleResultsFound as e:
			raise tornado.web.HTTPError(500)
		except sqlalchemy.orm.exc.NoResultsFound as e:
			raise tornado.web.HTTPError(404)

		return photo_repr(p)

	def patch(self, id=None):
		session = models.Session()

		try:
			p = session.query(models.Photo).filter_by(id=id).one()
		except sqlalchemy.orm.exc.MultipleResultsFound as e:
			raise tornado.web.HTTPError(500)
		except sqlalchemy.orm.exc.NoResultsFound as e:
			raise tornado.web.HTTPError(404)

		if "root" in self.json_args:
			p.root_hash = hashlib.md5(self.json_args["root"]).hexdigest()
			p.root = self.json_args["root"]
		if "rel_path" in self.json_args:
			p.rel_path = self.json_args["rel_path"]

		session.commit()

		return photo_repr(p)
