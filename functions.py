import re
import pandas as pd
from datetime import datetime, timedelta


def convert_to_hhmmss(duration):
    
    match = re.match(r'(?:(\d+)h)?\s*(?:(\d+)m)?', duration.strip())
    if not match:
        return "00:00:00"  
    
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    
    return f"{hours:02d}:{minutes:02d}:00"


def convert_to_hhmmss_v2(value):
    if pd.isna(value):
        return None
    value = value.strip()
    # if it already has seconds, return as-is
    if len(value.split(':')) == 3:
        return value
    # otherwise add ":00" for seconds
    return f"{value}:00"


def calculate_duration(dep, arr):
    
    def parse_time(t):
        t = t.strip()
        
        for fmt in ('%H:%M:%S', '%H:%M'):
            try:
                return datetime.strptime(t, fmt)
            except ValueError:
                continue
        raise ValueError(f"Time format not recognized: {t}")

    dep_dt = parse_time(dep)
    arr_dt = parse_time(arr)

    
    if arr_dt < dep_dt:
        arr_dt += timedelta(days=1)

    duration = arr_dt - dep_dt
    return str(duration)