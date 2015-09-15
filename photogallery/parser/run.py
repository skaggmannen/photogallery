import datetime
import hashlib
import logging
import multiprocessing
import os
import re
import time

log = logging.getLogger(__name__)

import PIL
import PIL.ExifTags

from photogallery.common import config, models
from photogallery.parser import exif

file_includes = "|".join([
	r"^.*\.jpg$",
	r"^.*\.JPG$",
])

file_excludes = "|".join([
	r"^\..+$",
])

dir_excludes = "|".join([
	r"^\..+$",
])

def photo_path(folder, photo):
	return os.path.join(folder, photo.dir, photo.name)

def read_md5(photo_details):
	path, md5 = photo_details
	try:
		f = open(path, "rb")
		m = hashlib.md5()
		m.update(f.read())
		f.close()
		return m.hexdigest()
	except IOError as e:
		return None

def create_thumb(photo_details):
	path, md5 = photo_details

	if md5 is None:
		return

	thumb_path = os.path.join(config.THUMBS_DIR, md5 + ".jpg")
	if os.path.exists(thumb_path):
		return

	try:
		i = PIL.Image.open(path)
		i.thumbnail(config.THUMBS_SIZE)
		i.save(thumb_path)
	except IOError as e:
		return

pool = multiprocessing.Pool()
def pool_job(fn, folder, photos):
	return [fn((photo_path(folder, p), p.md5)) for p in photos]

def scan_folder(folder):
	session = models.Session()
	for root, dirs, files in os.walk(folder.path):
		log.info("Scanning: %s", root)
		dir = os.path.relpath(root, folder.path)
		query = session.query(models.Photo).filter_by(folder_id=folder.id, dir=dir)

		existing = [photo.name for photo in query.all()]
		log.info("Existing: %s", ", ".join(existing))

		dirs[:] = [os.path.relpath(os.path.join(root, d), folder.path) for d in dirs if not re.match(dir_excludes, d)]
		log.info("Dirs: %s", ", ".join(dirs))

		photos = []

		for f in files:
			log.info("Checking file: %s", f)
			path = os.path.join(root, f)
			if not re.match(file_includes, f):
				log.debug("File does not match include patterns")
				continue
			if re.match(file_excludes, f):
				log.debug("File matches exclude pattern")
				continue
			if f in existing:
				log.debug("File already added")
				continue

			log.info("Adding file: %s", path)
			photo = models.Photo()
			photo.dir = dir
			photo.name = f
			photo.folder_id = folder.id

			photos.append(photo)

		if len(photos) == 0:
			continue

		pool = multiprocessing.Pool()
		log.info("Calculating MD5s...")
		for i, md5 in enumerate(pool_job(read_md5, folder.path, photos)):
			if md5 is None:
				log.error("MD5 calc failed for file: %s", photo_path(folder.path, photo))
			photos[i].md5 = md5

		log.info("Reading EXIF...")
		for i, info in enumerate(pool_job(exif.read, folder.path, photos)):
			if  info is None:
				continue

			orientation, date_time, year, month = info
			photos[i].orientation = orientation
			photos[i].date_time = date_time
			photos[i].year = year
			photos[i].month = month

		log.info("Creating thumbs...")
		seen = set()
		unique_photos = [p for p in photos if not p.md5 is None]
		unique_photos = [p for p in unique_photos if not p.md5 in seen or seen.add(p.md5)]
		pool_job(create_thumb, folder.path, unique_photos)

		session.add_all(photos)
		session.commit()

def run():
	session = models.Session()
	folders = session.query(models.Folder).all()
	for folder in folders:
		log.info("Scanning folder: %s", folder.path)
		scan_folder(folder)


if __name__ == "__main__":
	import sys

	config.init()
	models.init()

	if "purge" in sys.argv:
		response = raw_input("This will purge all photos. Type YES to Continue: ")
		if response == "YES":
			log.info("Purging all photos...")
			session = models.Session()
			session.query(models.Photo).delete()
			session.commit()

	run()