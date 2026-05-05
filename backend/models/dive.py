from sqlalchemy import Column,Integer,Float,String,DateTime,Text,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Dive(Base):
    __tablename__="dives"
    id = Column(Integer, primary_key=True,autoincrement=True)
    date = Column(DateTime)
    site = Column(String)
    location = Column(String)
    buddy = Column(String)
    

    max_depth_m = Column(Float)
    avg_depth_m = Column(Float)

    duration_s = Column(Integer)

    avg_temp_c = Column(Float)
    min_temp_c = Column(Float)
    max_temp_c = Column(Float)

    tank_start_bar = Column(Float)
    tank_end_bar = Column(Float)
    tank_size_l = Column(Float)
    avg_sac = Column(Float)

    visibility = Column(String)
    weather = Column(String)
    notes = Column(Text)

    profil_points = relationship("ProfilePoint", back_populates="dive",cascade="all,delete-orphans")

    equipement = relationship("Equipement", secondary="dive_equipement",back_populates="dives")

    