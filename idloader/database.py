from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker

# TODO: better path/project root dir management
engine = create_engine("sqlite:///idloader.db")
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Mod(Base):
    __tablename__ = "mod"

    mod_id = Column(String)
    mod_md5sum = Column(String, primary_key=True)
    mod_title = Column(String)
    mod_type = Column(String)
    mod_size_megabytes = Column(Integer)
    mod_authors = Column(String)
    mod_description = Column(String)
    mod_date = Column(String)
    mod_rating = Column(Integer)
    mod_screenshot = Column(String)
    PrimaryKeyConstraint("mod_md5sum", name="mod_pk")
