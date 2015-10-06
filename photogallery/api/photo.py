import logging

log = logging.getLogger(__name__)

import sqlalchemy
import tornado.web

from photogallery.common import config, models
from photogallery.api import JsonRequestHandler, photo_repr
	
class PhotoListHandler(JsonRequestHandler):
	url = r"/photo/"

	def get(self):
		session = models.Session()

		photos = session.query(models.Photo)
		total_count = None

		try:
			limit = self.get_query_argument("limit", default=100)
			offset = self.get_query_argument("offset", default=0)
			year = self.get_query_argument("year", default=None)
			month = self.get_query_argument("month", default=None)

			if year is not None:
				photos = photos.filter(models.Photo.year==int(year))
			if month is not None:
				photos = photos.filter(models.Photo.month==int(month))

			total_count = photos.count()

			photos = photos.order_by(models.Photo.date_time)
			photos = photos.limit(int(limit)).offset(int(offset))

		except ValueError as e:
			raise tornado.web.HTTPError(400)

		# Do a join on the limited set
		photos = photos.from_self(models.Photo, models.Folder)

		self.write({
			"total_count": total_count,
			"photos": [photo_repr(p, f) for p, f in photos.all()]
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
