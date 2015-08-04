import logging
import os
import re

log = logging.getLogger(__name__)

from photogallery.common import models

file_includes = "|".join([
	r".*\.jpg$",
	r".*\.JPG$",
])

file_excludes = "|".join([
	r"^\..+$",
])

dir_excludes = "|".join([
	r"^\..+$",
])

def exlude_dir(dir):
	for p in exlude_dir_patterns:
		if re.match(p, dir) is not None:
			return True
	return False

def scan_folder(folder):
	session = models.Session()
	for root, dirs, files in os.walk(folder.path):
		log.info("Scanning: %s", root)

		existing = session.query(models.Photo).filter_by(folder_id=folder.id, dir=os.path.relpath(root, folder.path)).all()
		log.info("Existing: %s", ", ".join(existing))

		dirs[:] = [os.path.relpath(os.path.join(root, d), folder.path) for d in dirs if not re.match(dir_excludes, d)]
		files = [os.path.relpath(os.path.join(root, f), folder.path) for f in files if re.match(file_includes, f) and not re.match(file_excludes, f)]

		log.info("Dirs: %s", ", ".join(dirs))
		log.info("Files: %s", ", ".join(files))

def run():
	session = models.Session()
	folders = session.query(models.Folder).all()
	for folder in folders:
		log.info("Scanning folder: %s", folder.path)
		scan_folder(folder)