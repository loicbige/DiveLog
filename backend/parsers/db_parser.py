from datetime import datetime
import sqlite3, json




def parse_shearwater(file_path: str):
    db = sqlite3.connect(file_path)
    db.row_factory = sqlite3.Row
    rows_dive_details = db.execute("SELECT * FROM dive_details").fetchall()
    calculated = db.execute("SELECT * FROM log_data").fetchall()
    db.close()

    log_date_dict = {}
    dive_details = []
    
    for l in calculated:
        log_date_dict[l["log_id"]] = json.loads(l["calculated_values_from_samples"])
    for r in rows_dive_details:
        logs = log_date_dict.get(r["DiveId"],{})
        dive_details.append({
            "date": datetime.strptime(r["DiveDate"], "%Y-%m-%d %H:%M:%S") if r["DiveDate"] else None,
            "max_depth_m": float(r["Depth"].replace(",",".")) if  r["Depth"] else None,
            "avg_depth_m": logs.get("AverageDepth"),
            "avg_temp_c": logs.get("AverageTemp"),
            "min_temp_c": logs.get("MinTemp"),
            "max_temp_c": logs.get("MaxTemp"),
            "duration_s": r["DiveLengthTime"],
            "site": r["Site"],
            "location": r["Location"],
            "buddy": r["Buddy"],
            "visibility": r["Visibility"],
            "weather": r["Weather"],
            "notes": r["Notes"],
            "weight_kg": float(r["Weight"].replace("kg", "").strip()) if r["Weight"] else None
        })
    return dive_details
    

