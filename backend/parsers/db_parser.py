from datetime import datetime
import sqlite3


def parse_shearwater(file_path: str):
    db = sqlite3.connect(file_path)
    db.row_factory = sqlite3.Row
    rows = db.execute("SELECT * FROM dive_details").fetchall()
    db.close()

    result = []
    for r in rows:
        result.append({
            "date": datetime.strptime(r["DiveDate"], "%Y-%m-%d %H:%M:%S") if r["DiveDate"] else None,
            "max_depth_m": float(r["Depth"].replace(",",".")) if  r["Depth"] else None,
            "avg_depth_m": r["AverageDepth"],
            "avg_temp_c": r["AverageTemp"],
            "min_temp_c": r["MinTemp"],
            "max_temp_c": r["MaxTemp"],
            "duration_s": r["DiveLengthTime"],
            "site": r["Site"],
            "location": r["Location"],
            "buddy": r["Buddy"],
            "visibility": r["Visibility"],
            "weather": r["Weather"],
            "notes": r["Notes"],
            "weight_kg": float(r["Weight"].replace("kg", "").strip()) if r["Weight"] else None
        })
    return result
    

