import json

import tornado.web

class JsonRequestHandler(tornado.web.RequestHandler):

	def prepare(self):
		if self.request.body is None:
			return

		if "application/json" not in self.request.headers.get("Content-Type", ""):
			raise tornado.web.HTTPError(415)

		try:
			self.json_args = json.loads(self.request.body)
		except ValueError as e:
			raise tornado.web.HTTPError(400)
