from pydantic import BaseModel
from typing import Optional

import datetime

class DiveCreate(BaseModel):
    
      date: datetime.datetime
      site: Optional[str] = None
      location: Optional[str] = None
      buddy: Optional[str] = None
      max_depth_m: float
      avg_depth_m: Optional[float] = None
      duration_s: int
      avg_temp_c: Optional[float] = None
      min_temp_c: Optional[float] = None
      max_temp_c: Optional[float] = None
      tank_start_bar: Optional[float] = None
      tank_end_bar: Optional[float] = None
      tank_size_l: Optional[float] = None
      visibility: Optional[str] = None
      weather: Optional[str] = None
      notes: Optional[str] = None

class DiveUpdate(BaseModel):
      date: Optional[datetime.datetime] = None
      site: Optional[str] = None
      location: Optional[str] = None
      buddy: Optional[str] = None
      max_depth_m: Optional[float] = None
      avg_depth_m: Optional[float] = None
      duration_s: Optional[int] = None
      avg_temp_c: Optional[float] = None
      min_temp_c: Optional[float] = None
      max_temp_c: Optional[float] = None
      tank_start_bar: Optional[float] = None
      tank_end_bar: Optional[float] = None
      tank_size_l: Optional[float] = None
      visibility: Optional[str] = None
      weather: Optional[str] = None
      notes: Optional[str] = None