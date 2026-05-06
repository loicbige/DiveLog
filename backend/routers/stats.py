from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.dive import Dive
from datetime import timedelta, datetime

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/surface-interval")
def get_surface_interval(db: Session = Depends(get_db)):
    last_dive = db.query(Dive).order_by(Dive.date.desc()).first()
    if last_dive is None:
        raise HTTPException(status_code=404, detail="Dive not found")
    
    end_date = last_dive.date + timedelta(seconds=last_dive.duration_s)
    int_surf =  datetime.now() - end_date
    
    tot_sec = int_surf.total_seconds()

    hours = int(tot_sec // 3600)
    if hours < 24:
        minutes = int((tot_sec%3600)//60)
        seconds = int((tot_sec%60))
        return {"hours": hours, "minutes": minutes, "seconds": seconds}

    else:
        days = int(tot_sec//86400)
        hours = int((tot_sec%86400) // 3600)
        minutes = int((tot_sec%3600) // 60)
        return {"days": days, "hours":hours, "minutes": minutes}


@router.get("/dives-number")
def get_dive_nb(db: Session = Depends(get_db)):
    return {"total_dives": db.query(Dive).count()}

@router.get("/time-underwater")
def get_time_underwater(db : Session = Depends(get_db)):
    
    tot_sec = db.query(func.sum(Dive.duration_s)).scalar()
    hours = int(tot_sec // 3600)
    if hours < 24:
        minutes = int((tot_sec%3600)//60)
        seconds = int((tot_sec%60))
        return {"hours": hours, "minutes": minutes, "seconds": seconds}

    else:
        days = int(tot_sec//86400)
        hours = int((tot_sec%86400) // 3600)
        minutes = int((tot_sec%3600) // 60)
        return {"days": days, "hours":hours, "minutes": minutes}
    
@router.get("/average-sac")
def get_avg_sac(db: Session = Depends(get_db)):
    avg = db.query(func.avg(Dive.avg_sac)).scalar()
    if avg is None:
        raise HTTPException(status_code=404,detail="cannot_calcluate_average_sac")
    
    return {"average_sac": round(avg,2)}


@router.get("/max-depth-reached")
def get_max_depth_reached(db: Session = Depends(get_db)):
    max_depth = db.query(func.max(Dive.max_depth_m)).scalar()
    return {"max_depth_reached": max_depth}

