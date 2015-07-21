import os

from settings import DB_STRING, DEBUG

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, exc

engine = create_engine(DB_STRING, echo=DEBUG)

Base = declarative_base()
Session = sessionmaker(bind=engine)

from sqlalchemy import Column, DateTime, String, Integer

class Photo(Base):
	__tablename__ = 'photo'
	id = Column(Integer, primary_key=True)
	root = Column(String)
	root_hash = Column(String)
	rel_path = Column(String)

	# Convenience fields for filtering
	year = Column(Integer)
	month = Column(Integer)

	# Extracted from EXIF
	orientation = Column(Integer)
	date_time = Column(DateTime)

	def __repr__(self):
		return "Photo<id={1},path={2}>".format(self.id, os.path.join(self.root, self.rel_path))