from photogallery.common import config, models

if __name__ == "__main__":
	config.init()
	models.init()

	session = models.Session()

	session.query(models.Photo).delete()

	session.commit()
