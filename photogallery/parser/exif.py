import datetime
import logging
import os

logger = logging.getLogger(__name__)

import PIL
import PIL.Image
import PIL.ExifTags


def read(photo_details):
	path, md5 = photo_details
	try:
		i = PIL.Image.open(path)
		exif = {
			PIL.ExifTags.TAGS[k]: v
			for k, v in i._getexif().items()
			if k in PIL.ExifTags.TAGS
		}
		del i

		timestamp = \
			exif.get("DateTimeOriginal", False) or \
			exif.get("DateTimeDigitized", False) or \
			exif.get("DateTime", False) or \
			None

		if timestamp is None:
			logger.info("EXIF date not found for image %s", path)
			secs = os.path.getctime(path)
			timestamp = datetime.datetime.fromtimestamp(secs)
		else:
			timestamp = datetime.datetime.strptime(timestamp, "%Y:%m:%d %H:%M:%S")

		return (
			exif.get("Orientation", 0),
			timestamp,
			timestamp.year,
			timestamp.month
		)
	except IOError as e:
		return None