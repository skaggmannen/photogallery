import logging

log = logging.getLogger(__name__)


import sqlalchemy
import tornado.web

from photogallery.common import config, models
from photogallery.api import JsonRequestHandler, photo_repr

def date_list_repr(dates):
	return {
		"dates": [
			{
				"year": y,
				"month": m,
			}
			for y, m in dates
		]
	}

class DateListHandler(JsonRequestHandler):
	url = r'/date/'

	def get(self):
		session = models.Session()
		dates = session.query(models.Photo.year, models.Photo.month).distinct().all()

		self.write(date_list_repr(dates))
		self.finish()


