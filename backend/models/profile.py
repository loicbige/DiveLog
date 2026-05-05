from sqlalchemy import Column,Integer,Float,ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class ProfilePoint(Base):
    __tablename__="profile_points"

    id = Column(Integer,primary_key=True, autoincrement=True)

    dive_id = Column(Integer,ForeignKey("dives.id"))
    time_s = Column(Integer)
    depth_m = Column(Float)
    temp_c = Column(Float)
    
    dive = relationship("Dive", back_populates="profile_points")
    