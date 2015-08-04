from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from photogallery.common import config

Base = declarative_base()
Session = sessionmaker()

class Folder(Base):
	__tablename__ = 'folder'
	id = Column(Integer, primary_key=True)
	path = Column(String)
	hash = Column(String)

class Photo(Base):
	__tablename__ = 'photo'
	id = Column(Integer, primary_key=True)
	folder_id = Column(Integer, ForeignKey('folder.id'))
	dir = Column(String)
	name = Column(String)

	# Convenience fields for filtering
	year = Column(Integer)
	month = Column(Integer)

	# Extracted from EXIF
	orientation = Column(Integer)
	date_time = Column(DateTime)

	def __repr__(self):
		return "Photo<id={1},path={2}>".format(self.id, os.path.join(self.root, self.rel_path))


def init():
	engine = create_engine(config.DB_STRING)
	Session.configure(bind=engine)
	Base.metadata.create_all(engine)