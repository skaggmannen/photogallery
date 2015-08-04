from distutils.core import setup

setup(
	name="PhotoGallery",
	version="0.0.1",
	author="Fredrik Allansson",
	author_email="fredrik.allansson@gmail.com",
	packages=["photogallery"],
	include_package_data=True,
	url="https://github.com/skaggmannen/photogallery",
	description="A Photo Gallery Web App",
	install_requires=[
		"Pillow",
		"sqlalchemy",
		"tornado",
	],
)
