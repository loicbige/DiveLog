from sqlalchemy import Column,Float, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base

class Tank(Base):
    __tablename__ = "tanks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    dive_id = Column(Integer, ForeignKey("dives.id"))
    equipement_id = Column(Integer, ForeignKey("equipement.id"))
    
    name = Column(String)
    tank_num = Column(Integer)
    tank_start_bar = Column(Float)
    tank_end_bar = Column(Float)
    tank_size_l = Column(Float)
    o2_percent = Column(Float)
    he_percent = Column(Float)

    dive = relationship("Dive",back_populates="tanks")
    equipement = relationship("Equipement", back_populates="tanks")

    