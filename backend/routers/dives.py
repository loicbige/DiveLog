from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from database import get_db
from models.dive import Dive
from schemas.dive import DiveCreate
router = APIRouter(prefix="/dives", tags=["dives"])


@router.get("/")
def get_dives(db: Session = Depends(get_db)):
    return db.query(Dive).all()

@router.get("/{dive_id}")
def get_dive_id(dive_id: int ,db: Session = Depends(get_db)):
        
        dive = db.query(Dive).filter(Dive.id == dive_id).first()
        if dive is None:
              raise HTTPException(status_code=404, detail="unknown_dive_id")
        else:
              return dive
        

@router.post("/", status_code=201)
def create_dive(dive_data: DiveCreate, db: Session = Depends(get_db)):
            dive = Dive(**dive_data.model_dump())
            db.add(dive)
            db.commit()
            db.refresh(dive)
            return dive