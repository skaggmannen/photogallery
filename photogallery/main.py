import md5
import os

from flask import request
from flask.ext.api import FlaskAPI, exceptions, status

from models import Photo, Base, engine, Session, exc

app = FlaskAPI(__name__)

def photo_repr(p):
	return {
		"url": "/api/v1/photos/{}".format(p.id),
		"image_url": "/static/{}/{}".format(p.root_hash, p.rel_path),
		"root": p.root,
		"rel_path": p.rel_path,
	}

@app.route("/api/v1/photos/", methods=["GET", "POST"])
def photo_list():
	session = Session()
	if request.method == "GET":
		return [photo_repr(p) for p in session.query(Photo)]

	if request.method == "POST":
		if isinstance(request.data, dict):
			data = [request.data]
		else:
			data = request.data

		photos = []

		for d in data:
			root_hash = md5.new(d.get("root")).hexdigest()

			p = Photo(root=d.get("root"), root_hash=root_hash, rel_path=d.get("rel_path"))
			session.add(p)
			photos.append(p)

		session.commit()

		return [{"url": "/api/v1/photos/{}".format(p.id)} for p in photos], status.HTTP_201_CREATED

@app.route("/api/v1/photos/<int:id>", methods=["GET", "PATCH", "DELETE"])
def photo_details(id):
	session = Session()

	print(id)

	try:
		p = session.query(Photo).filter_by(id=id).one()
	except exc.MultipleResultsFound:
		return {"error": "Multiple instance of photo with id {}".format(id)}, status.HTTP_500_INTERNAL_SERVER_ERROR
	except exc.NoResultFound:
		raise exceptions.NotFound()

	if request.method == "GET":
		return photo_repr(p)

	elif request.method == "PATCH":
		if "root" in request.data:
			p.root_hash = md5.new(request.data.get("root"))
			p.root = request.data.get("root")
		if "rel_path" in request.data:
			p.rel_path = request.data.get("rel_path")

		session.commit()

		return photo_repr(p)

	elif request.method == "DELETE":
		session.delete(p)
		session.commit()
		return '{}', status.HTTP_204_NO_CONTENT

if __name__ == "__main__":
	Base.metadata.create_all(engine)
	app.run(debug=True)
