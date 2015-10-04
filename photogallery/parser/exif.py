import datetime
import logging
import os
import sys

log = logging.getLogger(__name__)

import PIL
import PIL.Image
import PIL.ExifTags


def read(path):
	try:
		timestamp = None
		orientation = 1
		try:
			i = PIL.Image.open(path)
			exif = i._getexif()
			if exif is not None:
				exif = {
					PIL.ExifTags.TAGS[k]: v
				for k, v in exif.items()
				if k in PIL.ExifTags.TAGS
			}

			timestamp = \
				exif.get("DateTimeOriginal", False) or \
				exif.get("DateTimeDigitized", False) or \
				exif.get("DateTime", False) or \
				None
			orientation = exif.get("Orientation", 1)
			del i
		except:
			e = sys.exc_info()[0]
			log.error("Failed to read exif: %s", e)

		if timestamp is not None:
			patterns = ["%Y:%m:%d %H:%M:%S", "%Y:%m:%d %H:%M: %S"]
			for p in patterns:
				try:
					timestamp = datetime.datetime.strptime(timestamp, p)
					break
				except ValueError as e:
					log.warn(e)
					pass
			else:
				log.warn("%s didn't match any pattern", timestamp)
				timestamp = None

		if timestamp is None:
			log.info("EXIF date not found for image %s", path)
			secs = os.path.getctime(path)
			timestamp = datetime.datetime.fromtimestamp(secs)

		return (
			orientation,
			timestamp
		)
	except IOError as e:
		return (None, None)
