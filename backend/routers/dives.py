from fastapi import APIRouter,HTTPException,Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models.dive import Dive
from schemas.dive import DiveCreate, DiveUpdate
from parsers.db_parser import parse_shearwater

import tempfile,shutil


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


@router.put("/{dive_id}")
def update_dive(dive_id: int,dive_data: DiveUpdate,db: Session = Depends(get_db)):
    dive = db.query(Dive).filter(Dive.id == dive_id).first()
    
    if dive is None:
         raise HTTPException(status_code=404, detail="unknown_dive_id")
    
    for key,value in dive_data.model_dump(exclude_unset=True).items():
        setattr(dive, key, value)
    
    
    db.commit()
    db.refresh(dive)
    
    return dive
    

@router.delete("/{dive_id}", status_code=204)
def delete_dive(dive_id: int, db: Session = Depends(get_db)):
    dive = db.query(Dive).filter(Dive.id == dive_id).first()
    if dive is None:
         raise HTTPException(status_code=404, detail="unknown_dive_id")
    db.delete(dive)
    db.commit()


@router.post("/import")
def import_dive(file: UploadFile = File(...), db: Session = Depends(get_db)):
     
     with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
          shutil.copyfileobj(file.file, tmp)
          tmp_path = tmp.name
     dives = parse_shearwater(tmp_path)
     for d in dives:
          toAdd = Dive(**d)
          db.add(toAdd)
          db.commit()
          db.refresh(toAdd)          
     return {"imported" : len(dives)}


