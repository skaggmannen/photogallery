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

def read_md5(path):
	try:
		f = open(path, "rb")
		m = hashlib.md5()
		m.update(f.read())
		f.close()
		return m.hexdigest()
	except IOError as e:
		log.error("MD5 calc failed for file: %s", path)
		return None

def create_thumb(path, md5):
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
		log.error("Failed to create thumb for file %s", path)
		return
	except IndexError as e:
		log.error("Failed to create thumb for file %s", path)
		return

def scan_folder(folder):
	session = models.Session()
	for root, dirs, files in os.walk(folder.path):
		log.info("Scanning: %s", root)
		dir = os.path.relpath(root, folder.path)
		query = session.query(models.Photo).filter_by(folder_id=folder.id, dir=dir)

		existing = [photo.name for photo in query.all()]
		log.debug("Existing: %s", ", ".join(existing))

		dirs[:] = [
			d
			for d in dirs 
			if not re.match(dir_excludes, d)
		]

		log.debug("Dirs: %s", ", ".join(dirs))

		files_added = 0
		for f in files:
			log.debug("Checking file: %s", f)
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

			log.debug("Adding file: %s", path)

			photo = models.Photo()
			photo.dir = dir
			photo.name = f
			photo.folder_id = folder.id
			photo.md5 = read_md5(path)
			photo.orientation, photo.date_time = exif.read(path)
			if photo.orientation is None or photo.date_time is None:
				log.error("Skipping %s due to errors...", path)
				continue

			photo.year = photo.date_time.year
			photo.month = photo.date_time.month

			create_thumb(path, photo.md5)

			session.add(photo)
			session.commit()

			files_added += 1

		log.info("Added %d new files...", files_added)

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
