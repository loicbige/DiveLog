from sqlalchemy import Column,Integer, Text, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Equipement(Base):
    
    __tablename__="equipement"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    category = Column(String)
    serial_number = Column(String)
    purchase_date = Column(DateTime)
    last_service_date = Column(DateTime)
    notes = Column(Text)
    dives = relationship("Dive",secondary="dive_equipement", back_populates="equipement")
class DiveEquipement(Base):
    __tablename__="dive_equipement"
    dive_id = Column(Integer, ForeignKey("dives.id"), primary_key=True)
    equipement_id = Column(Integer,ForeignKey("equipement.id"), primary_key=True)


