import json
import os

import tornado.web

from photogallery.common import config

def photo_repr(p, f):
	if p.dir != "":
		rel_path = os.path.join(p.dir, p.name).encode("utf-8")
	else:
		rel_path = p.name

	return {
		"url": config.API_URL_BASE + "/photo/{0}".format(p.id),
		"image": "/dynamic/{0}/{1}".format(f.hash, rel_path),
		"thumb": "/thumbs/{0}.jpg".format(p.md5),
		"date_time": p.date_time.strftime("%Y-%m-%d %H:%M:%S"),
		"orientation": p.orientation,
		"path": os.path.join(f.path, p.dir, p.name).encode("utf-8"),
	}

class JsonRequestHandler(tornado.web.RequestHandler):

	def prepare(self):
		if len(self.request.body) == 0:
			return

		if "application/json" not in self.request.headers.get("Content-Type", ""):
			raise tornado.web.HTTPError(415)

		try:
			self.json_args = json.loads(self.request.body)
		except ValueError as e:
			raise tornado.web.HTTPError(400)

# This needs to be last since it requires JsonRequestHandler
import photo